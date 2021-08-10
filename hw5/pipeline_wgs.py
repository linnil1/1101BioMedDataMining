from utils import run, docker_run, docker_build

# --- Docker Image --- #
# downloaded qqman not work
# image_qqman = "quay.io/biocontainers/r-qqman:0.1.4--r36h6115d3f_4"
# self-build qqman work
image_qqman = "linnil1/qqman"
dockerfile_qqman = "docker_qqman.dockerfile"

# plink1.9 used in letture
# image_plink = "quay.io/biocontainers/plink:1.90b4--h0a6d026_2"
# plink2 for this pipeline
image_plink = "quay.io/biocontainers/plink2:2.00a2.3--hf22980b_0"

# --- Data --- #
name = "data/example_wgs"
# two data are not available online
# * "data/example_wgs.vcf"  # a variant calling file(After normalized)
# * "data/example_wgs.csv"  # phenotype file


# --- Import vcf and phenotype --- #
def weg_import():
    docker_run(image_plink,
               f"plink2 --make-pgen "
               f"--vcf {name}.vcf.gz --pheno {name}.csv "
               f"--out {name}.plink")


# --- Filter the genotype and sample --- #
def wgs_filter():
    docker_run(image_plink,
               f"plink2 --make-pgen --pfile {name} "
               # Missing for one sample > 0.2 -> delete sample
               "--mind 0.2 "
               # Missing allele > 0.2  -> delete allele
               "--geno 0.2 "
               # minor allele freq < 0.08 -> delete allele
               "--maf 0.08 "
               # Hardy-Weinberg Equilibrium p-value < 1e-6 -> reject
               "--hwe 1e-6 "
               f"--out {name}.filter")


# --- Regression --- #
def wgs_regression():
    docker_run(image_plink,
               f"plink2 --make-pgen --pfile {name} "
               f"--glm --out {name}.assoc")
    run(f"ln -s {name.split('/')[1]}.PHENOTYPE.glm.logistic {name}.csv")


# --- Plot --- #
def wgs_plot():
    docker_run(image_qqman, f"Rscript draw_manhattan.R {name}")


if __name__ == "__main__":
    wgs_import()
    name += ".plink"
    wgs_filter()
    name += ".filter"
    wgs_regression()
    name += ".assoc"
    docker_build(image_qqman, dockerfile_qqman)
    wgs_plot()
