from pipeline_1 import *


hg38              = "data/GRCh38_latest_genomic"
image_fastqc      = "quay.io/biocontainers/fastqc:0.11.9--0"
image_trimmomatic = "quay.io/biocontainers/trimmomatic:0.39--hdfd78af_2"
image_hisat       = "quay.io/biocontainers/hisat2:2.2.1--he1b5a44_2"
image_samtool     = "quay.io/biocontainers/samtools:1.10--h9402c20_2"
image_stringtie   = "quay.io/biocontainers/stringtie:2.1.7--h978d192_0"
image_deseq2      = "quay.io/biocontainers/bioconductor-deseq2:1.28.0--r40h5f743cb_0"
image_gffcompare  = "quay.io/biocontainers/gffcompare:0.11.2--h7d875b9_2"

folder_fastqc     = "data/fastqc"
folder_hisat      = "hisat2/genome"
stringtie_list    = "data/merge.list"
stringtie_merge   = "data/merge.stringtie"
suffix = ""


def download():
    run(f"wget https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.fna.gz "
        f"-O {hg38}.fna.gz")
    run(f"gunzip {hg38}.fna.gz")
    run(f"wget https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.gff.gz "
        f"-O {hg38}.gff.gz")
    run(f"gunzip {hg38}.gff.gz")
    run(f"wget http://genomedata.org/rnaseq-tutorial/practical.tar "
        f"-O data/practical.tar")
    run(f"tar xf data/practical.tar -C data/")


def getSample():
    return [
        "data/hcc1395_normal_rep1",
        "data/hcc1395_normal_rep2",
        "data/hcc1395_normal_rep3",
        "data/hcc1395_tumor_rep1",
        "data/hcc1395_tumor_rep2",
        "data/hcc1395_tumor_rep3",
    ]


def fastqc():
    run(f"mkdir -p {folder_fastqc}")
    fastq = map(lambda i: i + '*' + suffix + '.fastq.gz', getSample())
    docker_run(image_fastqc,
               f"fastqc -t {thread} {' '.join(fastq)} -o {folder_fastqc}")


def trimmomatic():
    for name in getSample():
        docker_run(image_trimmomatic,
                   f"trimmomatic PE -threads {thread} "
                   f"{name}_r1.fastq.gz       {name}_r2.fastq.gz "
                   f"{name}_r1.clean.fastq.gz {name}_r1.unpair.fastq.gz "
                   f"{name}_r2.clean.fastq.gz {name}_r2.unpair.fastq.gz "
                   f"ILLUMINACLIP:./TruSeq3-PE.fa:2:30:10:2:keepBothReads "
                   f"LEADING:3 TRAILING:3 MINLEN:36")


def hisatInit():
    run(f"mkdir -p {folder_hisat}")
    docker_run(image_hisat,
               f"hisat2-build -p {thread} {hg38}.fna {folder_hisat}")


def hisatRun():
    for name in getSample():
        docker_run(image_hisat,
                   f"hisat2 -p {thread} --dta -x {folder_hisat} "
                   f"-1 {name}_r1{suffix}.fastq.gz -2 {name}_r2{suffix}.fastq.gz "
                   f"-S {name}{suffix}.hisat.sam")
        docker_run(image_samtool,
                   f"samtools sort -@ {thread} "
                   f"{name}{suffix}.hisat.sam -o {name}{suffix}.hisat.bam")


def stringtieRun():
    for name in getSample():
        docker_run(image_stringtie,
                   f"stringtie -p {thread} -G {hg38}.gff {name}{suffix}.bam "
                   f"-o {name}{suffix}.stringtie.gff")
    open(stringtie_list, "w").writelines(
         map(lambda i: i + suffix + ".stringtie.gff\n", getSample()))
    docker_run(image_stringtie,
               f"stringtie -p {thread} --merge -G {hg38}.gff {stringtie_list} "
               f"-o {stringtie_merge}.gff")
    for name in getSample():
        docker_run(image_stringtie,
                   f"stringtie -e -B -p {thread} -G {stringtie_merge}.gff "
                   f"{name}{suffix}.bam -o {name}{suffix}.stringtie.merge.gff")


def gffcompareRun():
    docker_run(image_gffcompare,
               f"gffcompare -r {hg38}.gff -G {stringtie_merge}.gff "
               f"-o {stringtie_merge}.compare")


def stringtieAfter():
    open(stringtie_list, "w").writelines(
        map(lambda i: f"{i}{suffix} {i}{suffix}.gff\n", getSample()))
    run(f"python3 prepDE.py -i {stringtie_list} "
        f"-g {stringtie_merge}.result.gene.csv -t {stringtie_merge}.result.tx.csv")


def deseqRun():
    docker_run(image_deseq2, f"Rscript deseq2.R {stringtie_merge}.result.tx")


if __name__ == "__main__":
    # download()
    # fastqc()
    # trimmomatic()
    suffix = ".clean"
    # fastqc()
    # hisatInit()
    # hisatRun()
    suffix = ".clean.hisat"
    # stringtieRun()
    # gffcompareRun()
    suffix = ".clean.hisat.stringtie.merge"
    # stringtieAfter()
    # deseqRun()
