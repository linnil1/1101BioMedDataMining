import os
import pandas as pd
import numpy as np
from utils import run, docker_run, docker_build
from pipeline_wgs import image_plink


image_geneepi = "linnil1/geneepi"
dockerfile_geneepi = "docker_geneepi.dockerfile"
name = "data/example_wgs.plink.filter"
geneepi_folder = "data/geneepi"
thread = 30


def plink_export_oxford(suffix):
    name_out = name + suffix
    docker_run(image_plink,
               f"plink2 --export oxford --pfile {name} "
               f"--out {name_out} --keep {name_out}.id.csv")
    # stupid format for Genepi
    pheno = pd.read_csv(f"{name_out}.sample", sep=" ", skiprows=[1])
    pheno[["PHENOTYPE"]].to_csv(f"{name_out}.sample.onlypheno.csv",
                                index=False, header=False)


def split_train_test():
    # get available samples (Missing already removed)
    docker_run(image_plink,
               f"plink2 --export oxford --pfile {name} --out {name}.tmp")

    # case 200    control 1000     <- origin
    # case 10     control 100      -> test
    # case 200-10 control 1000-100 -> control
    data = pd.read_csv(f"{name}.tmp.sample", sep=" ", skiprows=[1])

    id_case = np.where(data["PHENOTYPE"] == 0)[0]
    id_ctrl = np.where(data["PHENOTYPE"] == 1)[0]

    np.random.seed(20210807)
    id_test = np.hstack([
        np.random.choice(id_case, len(id_case) // 10, replace=False),
        np.random.choice(id_ctrl, len(id_ctrl) // 10, replace=False)])

    data.loc[id_test, "ID_2"]\
        .to_csv(f"{name}.test.id.csv", index=False, header=False)
    data.loc[set(data.index) - set(id_test), "ID_2"]\
        .to_csv(f"{name}.train.id.csv", index=False, header=False)


def geneepi():
    os.makedirs(geneepi_folder, exist_ok=True)
    name_out = name + ".train"
    docker_run(image_geneepi,
               f"GenEpi -t {thread} -g {name_out}.gen "
               f"-p {name_out}.sample.onlypheno.csv -o {geneepi_folder} ")
    name_out = name + ".test"
    docker_run(image_geneepi,
               f"python3 genepi_validation.py {name_out}.gen "
               f"{name_out}.sample.onlypheno.csv {geneepi_folder}")


if __name__ == "__main__":
    split_train_test()
    plink_export_oxford(".train")
    plink_export_oxford(".test")
    docker_build(image_geneepi, dockerfile_geneepi)
    geneepi()
