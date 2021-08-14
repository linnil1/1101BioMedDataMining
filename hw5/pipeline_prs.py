import os
import pandas as pd
import numpy as np
from utils import run, docker_run, docker_build
from pipeline_wgs import image_plink


image_geneepi = "linnil1/geneepi"
image_prscs = "linnil1/prscs"
dockerfile_geneepi = "docker_geneepi.dockerfile"
dockerfile_prscs = "docker_prscs.dockerfile"
# name = "data/example_wgs.plink.filter"
name = "data/HapMap_3_r3_1"
thread = 20
image_plink_old = "quay.io/biocontainers/plink:1.90b4--h0a6d026_2"


def download_hapmap():
    """ https://github.com/MareesAT/GWA_tutorial """
    run("wget https://github.com/MareesAT/GWA_tutorial/raw/master/1_QC_GWAS.zip -O data/1_QC_GWAS.zip")
    run(f"cd data && unzip 1_QC_GWAS.zip && cp 1_QC_GWAS/Hap* .")


def download_prscs():
    run("git clone https://github.com/getian107/PRScs.git")
    run("wget https://www.dropbox.com/s/7ek4lwwf2b7f749/ldblk_1kg_eas.tar.gz?dl=1 -O data/ldblk_1kg_eas.tar.gz")
    run("cd data && tar -zxvf data/ldblk_1kg_eas.tar.gz")


def createPlink():
    # read plink data
    docker_run(image_plink,
               f"plink2 --make-pgen --bfile {name} --sort-vars --not-chr X,XY "
               f"--out {name}.plink")
    # Calculate allele freq into {name].afreq
    docker_run(image_plink, f"plink2 -pfile {name} --freq --out {name}")


def plink_export_oxford(suffix):
    """ plink2 data -> plink1.9 data for GenEpi """
    name_out = name + suffix
    docker_run(image_plink,
               f"plink2 --export oxford --pfile {name} "
               f"--out {name_out} --keep {name_out}.id.csv")
    # stupid format for Genepi
    pheno = pd.read_csv(f"{name_out}.sample", sep=" ", skiprows=[1])
    pheno[["PHENO1"]].to_csv(f"{name_out}.sample.onlypheno.csv",
                             index=False, header=False)


def split_train_test():
    """ Split samples inot training and testing """
    # get samples and phenotype list from plink2
    docker_run(image_plink,
               f"plink2 --export oxford --pfile {name} --out {name}.tmp")
    data = pd.read_csv(f"{name}.tmp.sample", sep=" ", skiprows=[1])

    # remove N.A.
    data = data.dropna().reset_index()
    data["PHENO1"] = data["PHENO1"].astype(np.int)

    # origin 165 samples: 56 case, 56 control, other no phenotype
    # train   90 samples: 45 case, 45 control
    # test    22 samples: 11 case, 11 control
    np.random.seed(2021)
    id_case = np.where(data["PHENO1"] == 0)[0]
    id_ctrl = np.where(data["PHENO1"] == 1)[0]
    id_test = np.hstack([
        np.random.choice(id_case, len(id_case) // 5, replace=False),
        np.random.choice(id_ctrl, len(id_ctrl) // 5, replace=False)])

    # save samples list to csv
    data.loc[id_test, ["ID_1", "ID_2"]]\
        .to_csv(f"{name}.test.id.csv", index=False, header=False, sep="\t")
    data.loc[set(data.index) - set(id_test), ["ID_1", "ID_2"]]\
        .to_csv(f"{name}.train.id.csv", index=False, header=False, sep="\t")


def geneepi():
    """ https://github.com/Chester75321/GenEpi """
    geneepi_folder = name_out + ".geneepi"
    name_out = name + ".train"
    os.makedirs(geneepi_folder, exist_ok=True)

    # training
    # A trick to set chi-square test < 1e-4
    docker_run(image_geneepi,
               "bash -c \"sed -e 's/x > 5/x > 4/g' /usr/local/lib/python3.8/site-packages/genepi/step5_crossGeneEpistasis_Logistic.py -i && "
               f"GenEpi -t {thread} -g {name_out}.gen -k 5 "
               f"-p {name_out}.sample.onlypheno.csv -o {geneepi_folder} \"")

    # testing
    name_out = name + ".test"
    docker_run(image_geneepi,
               f"python3 genepi_validation.py {name_out}.gen "
               f"{name_out}.sample.onlypheno.csv {geneepi_folder}")


def plink_export_plink19(suffix):
    """ Output plink19 and old assoc format (training and testing) """
    name_out = name + suffix
    docker_run(image_plink,
               f"plink2 --make-bed --pfile {name} "
               f"--keep {name_out}.id.csv --out {name_out}.assoc")
    name_out += ".assoc"
    docker_run(image_plink_old,
               f"plink --assoc -bfile {name_out} --allow-no-sex "
               f"--out {name_out}.old")
    name_out += ".old"
    df = pd.read_csv(f"{name_out}.assoc", sep=r"\s+")
    df[["SNP", "A1", "A2", "OR", "P"]].dropna().to_csv(
            f"{name_out}.csv", sep=" ", index=False)


def prscs():
    """ https://github.com/getian107/PRScs """
    n_sample = len(pd.read_csv(f"{name}.train.id.csv", header=None))
    name_out = name + ".prscs"
    # this takes 40 * 22 mins
    # run(f"THREADS={thread} python3 PRScs/PRScs.py "
    docker_run(image_prscs,
               f"python3 /opt/PRScs.py "
               f"--ref_dir data/ldblk_1kg_eas "
               f"--bim_prefix {name}.train.assoc "
               f"--sst_file {name}.train.assoc.old.csv "
               f"--n_gwas {n_sample} --out_dir {name_out}",
               f"-e THREADS={thread}")
    run(f"cat {name_out}*.txt > {name_out}.merge.txt")

    # show prs
    df = pd.read_csv(f"{name_out}.merge.txt", sep="\t", header=None)
    df[6] = df[5].abs()
    print("PRScs first 10 highest weight")
    print(df.sort_values(6, ascending=False).iloc[:10, :6])

    # apply prs
    docker_run(image_plink,
               f"plink2 --bfile {name}.train.assoc "
               f"--read-freq {name}.afreq "
               f"--score {name_out}.merge.txt 2 4 6 "
               f"--out {name_out}.train.score")
    docker_run(image_plink,
               f"plink2 --bfile {name}.test.assoc "
               f"--read-freq {name}.afreq "
               f"--score {name_out}.merge.txt 2 4 6 "
               f"--out {name_out}.score")


def plink_prs():
    name_train = name + ".train.assoc"
    docker_run(image_plink,
               f"plink2 --make-pgen --bfile {name_train} "
               f"--glm --out {name_train}")
    df = pd.read_csv(f"{name_train}.PHENO1.glm.logistic", sep=r"\s+")
    df = df.dropna()
    df["BETA"] = np.log(df["OR"])
    df.to_csv(f"{name_train}.csv", sep=" ", index=False, header=False)

    # display
    print("Plink first 10 lowest P-value")
    print(df.sort_values("P", ascending=True).iloc[:10])

    # apply prs
    docker_run(image_plink,
               f"plink2 --bfile {name}.train.assoc "
               f"--read-freq {name}.afreq "
               f"--score {name_train}.csv 3 6 13 "
               f"--out {name}.plinkprs.train.score")
    docker_run(image_plink,
               f"plink2 --bfile {name}.test.assoc "
               f"--read-freq {name}.afreq "
               f"--score {name_train}.csv 3 6 13 "
               f"--out {name}.plinkprs.score")


def validation(title=""):
    import sklearn.metrics as skMetric
    import matplotlib.pyplot as plt
    data = pd.read_csv(f"{name}.sscore", sep="\t")

    # calculate ROC
    fpr, tpr, thresholds = \
        skMetric.roc_curve(data["PHENO1"] - 1, data["SCORE1_AVG"])
    float_auc = skMetric.auc(fpr, tpr)
    print(title, name)
    print(f"AUC:         {float_auc:.02f}")

    # plot it
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label=f'ROC curve (area = {float_auc:0.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Receiver operating characteristic of {title}')
    plt.legend(loc="lower right")
    plt.savefig(f"{name}.roc.png")


if __name__ == "__main__":
    download_hapmap()
    createPlink()
    name = name + ".plink"
    split_train_test()

    # Geneepi
    plink_export_oxford(".train")
    plink_export_oxford(".test")
    docker_build(image_geneepi, dockerfile_geneepi)
    geneepi()

    # prscs
    download_prscs()
    plink_export_plink19(".train")
    plink_export_plink19(".test")
    docker_build(image_prscs, dockerfile_prscs)
    prscs()  # takes 10hr to run

    # plink
    plink_prs()

    # validate prscs and plink
    base_name = name
    name = base_name + ".plinkprs.score"
    validation("plink_prs")
    # name = base_name + ".plinkprs.train.score"
    # validation("plink_prs train")  # -> AUC = 1
    name = base_name + ".prscs.score"
    validation("prscs")
    # name = base_name + ".prscs.train.score"
    # validation("prscs train")  # -> AUC = 1
