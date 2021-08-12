from utils import run, docker_run, docker_build, googleDownload
import pandas as pd
import os

# --- Docker Image --- #
image_fastqc      = "quay.io/biocontainers/fastqc:0.11.9--0"
image_trimmomatic = "quay.io/biocontainers/trimmomatic:0.39--hdfd78af_2"
image_samtool     = "quay.io/biocontainers/samtools:1.10--h9402c20_2"
image_bbmap       = "quay.io/biocontainers/bbmap:38.91--he522d1c_1"
image_bowtie      = "quay.io/biocontainers/bowtie2:2.4.4--py39hbb4e92a_0"
image_macs2       = "quay.io/biocontainers/macs2:2.2.7.1--py38h4a8c8d9_2"
image_bedtools    = "quay.io/biocontainers/bedtools:2.29.2--hc088bd4_0"
image_meme        = "quay.io/biocontainers/meme:5.3.0--py39pl5262heb7a276_2"
image_idr         = "quay.io/biocontainers/idr:2.0.4.2--py38hd504320_4"
image_ezgeno      = "linnil1/ezgeno"

# --- Data --- #
os.makedirs("data/", exist_ok=True)
folder_fastqc     = "data/fastqc"
file_adapter      = "data/TruSeq3-SE.fa"
file_exclude_peak = "data/ENCFF023CZC.bed.gz"
bowtie2_index     = "data/Homo_sapiens.GRCh38.dna.primary_assembly"
name_merge        = "data/ENCFF000YN.merge"
thread            = 20
suffix = ""


def getSample():
    return [
        "data/ENCFF000YNF",
        "data/ENCFF000YND",
        "data/ENCFF000YQC",
    ]


def download():
    os.chdir("data")
    # case
    # https://www.encodeproject.org/experiments/ENCSR000EFT/
    run("wget https://www.encodeproject.org/files/ENCFF000YNF/@@download/ENCFF000YNF.fastq.gz")
    run("wget https://www.encodeproject.org/files/ENCFF000YND/@@download/ENCFF000YND.fastq.gz")
    # control
    # https://www.encodeproject.org/experiments/ENCSR000EHM/
    run("wget https://www.encodeproject.org/files/ENCFF000YQC/@@download/ENCFF000YQC.fastq.gz")

    os.chdir("..")

    # download adapter
    run("wget https://raw.githubusercontent.com/timflutre/trimmomatic/master/adapters/TruSeq3-SE.fa"
        f" -O {file_adapter}")

    # excluded region
    run("wget https://www.encodeproject.org/files/ENCFF023CZC/@@download/ENCFF023CZC.bed.gz"
        f" -O {file_exclude_peak}")


def fastqc():
    os.makedirs(folder_fastqc, exist_ok=True)
    fastq = map(lambda name: name + suffix + '*.fastq.gz', getSample())
    docker_run(image_fastqc,
               f"fastqc -t {thread} {' '.join(fastq)} -o {folder_fastqc}")


def trimmomatic():
    """ Not neccessery in this case """
    for name in getSample():
        name_out = name + suffix
        docker_run(image_trimmomatic,
                   f"trimmomatic SE -threads {thread} "
                   f"{name_out}.fastq.gz {name_out}.trim.fastq.gz "
                   f"ILLUMINACLIP:{file_adapter}:2:40:12 "
                   f"LEADING:10 SLIDINGWINDOW:4:15 MINLEN:25")


def bbmapFilterTile():
    """ Qualiy per tile is bad shown in fastqc """
    for name in getSample():
        docker_run(image_bbmap,
                   f"filterbytile.sh in={name}{suffix}.fastq.gz "
                   f"out={name}{suffix}.trimtile.fastq.gz")
        # In this case, case will fail in this command
        if not os.path.exists(f"{name}{suffix}.trimtile.fastq.gz"):
            run(f"ln -s {name.split('/')[-1]}{suffix}.fastq.gz "
                f"{name}{suffix}.trimtile.fastq.gz")


def bowtiePre():
    """ Download reference sequence and build the index """
    run("wget http://ftp.ensembl.org/pub/release-104/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
        f" -O {bowtie2_index}.fa.gz")
    # build index
    docker_run(image_bowtie,
               f"bowtie2-build --threads {thread} {bowtie2_index}.fa.gz "
               f"{bowtie2_index} ")
    # build fasta index for meme
    run(f"gunzip -k {bowtie2_index}.fa.gz")
    docker_run(image_samtool, f"samtools faidx {bowtie2_index}.fa")


def bowtie():
    """ Read mapping and filer """
    for name in getSample():
        name_out = name + suffix
        docker_run(image_bowtie,
                   f"bowtie2 -p {thread} -x {bowtie2_index} "
                   f"-U {name_out}.fastq.gz -S {name_out}.bowtie.sam")
        # Remove secondary and sort
        name_out = name_out + ".bowtie"
        docker_run(image_samtool,
                   f"bash -c '"
                   f"samtools view -@{thread} -F 268 -q 5 -h {name_out}.sam | "
                   f"samtools sort -@{thread} -o {name_out}.filter.bam'")
        # Remove duplicated
        name_out = name_out + ".filter"
        docker_run(image_samtool,
                   f"samtools markdup -@{thread} -r "
                   f"{name_out}.bam {name_out}.dedup.bam")
        name_out = name_out + ".dedup"
        # Build bam index
        docker_run(image_samtool,
                   f"samtools index {name_out}.bam")


def macs2():
    """ Peak calling """
    control = getSample()[-1] + suffix
    for name in getSample()[:-1]:
        name_out = name + suffix
        docker_run(image_macs2,
                   f"macs2 callpeak -t {name_out}.bam -c {control}.bam -f BAM "
                   f"--gsize hs -n {name_out}.macs2")


def meme():
    """ Motif discovery by meme after some peak excluded """
    for name in getSample()[:-1]:
        # extend the summit files to flank=100
        name_out = name + suffix
        df = pd.read_csv(f"{name_out}_summits.bed", sep="\t", header=None)
        df[2] = df[1] + 100
        df[1] = df[1] - 100
        df.loc[df[1] < 1, 1] = 1
        df.to_csv(f"{name_out}.summit.extend.bed",
                  index=False, header=False, sep="\t")
        name_out = name_out + ".summit.extend"

        # Remove excluded region
        docker_run(image_bedtools,
                   f"bedtools subtract -a {name_out}.bed "
                   f"-b {file_exclude_peak} -A -nonamecheck "
                   f"> {name_out}.excluded.bed")
        name_out = name_out + ".excluded"

        # Pick by top 500 score region
        n_peak = 500
        pd.read_csv(f"{name_out}.bed", sep="\t", header=None) \
            .sort_values(4, ascending=False)[:n_peak] \
            .to_csv(f"{name_out}.top.bed", index=False, header=False, sep="\t")

        # Get top 500 score sequences
        name_out = name_out + ".top"
        docker_run(image_bedtools,
                   f"bedtools getfasta -bed {name_out}.bed "
                   f"-fi {bowtie2_index}.fa > {name_out}.peaks.fa")

        # motif discovery
        name_out = name_out + ".peaks"
        n_motif = 5
        docker_run(image_meme,
                   f"meme-chip -meme-nmotifs {n_motif} "
                   f"{name_out}.fa -oc {name_out}.meme")


def mergePeak():
    """ Merge narrowPeaks file """
    samples = []

    for name in getSample()[:-1]:
        # sort narrow peak by p-value
        name_in = name + suffix
        pd.read_csv(f"{name_in}_peaks.narrowPeak", sep="\t", header=None) \
            .sort_values(7, ascending=False) \
            .to_csv(f"{name_in}.peaks.sort.narrowPeak",
                    index=False, header=False, sep="\t")
        samples.append(f"{name_in}.peaks.sort.narrowPeak")

    # Select peak by false-discovery rate via IDR
    docker_run(image_idr, f""" \
               idr --samples {' '.join(samples)} \
               --input-file-type narrowPeak --rank p.value --plot \
               --output-file {name_merge}.idr \
               --log-output-file {name_merge}.idr.log""")


def ezgenoPre():
    """
    Prepare for ezgeno

    1. Build dockerfile
    2. Download sequences
    3. Separate data to train and test
        * ezgeno.train.seq
        * ezgeno.test.seq
        * ezgeno.pos.fa
    """
    os.chdir("data")
    # # Download data
    # # This sample is same as
    # # {name}.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.fa
    googleDownload("1dZnVMysb_5kTaJJX-oiO7beJUytT85GB")
    run("mv top_peaks.fa ezgeno.fa")

    # Separate odd row to train and even to test
    # put Sequences only data in ezgeno.pos.ga
    fin = open("ezgeno.fa")
    ftrain = open("ezgeno.train.seq", "w")
    ftest = open("ezgeno.test.seq", "w")
    fpos = open("ezgeno.pos.fa", "w")
    ftrain.write("FoldID\tEventID seq\tBound\t\n")
    ftest.write("FoldID\tEventID seq\tBound\t\n")
    num = 0
    for line in fin:
        if line[0] == ">":
            continue
        # 50 + 1 + 50
        seq = line[50:151]
        fpos.write(seq + "\n")
        txt = f"A\tseq_{num:05d}_peak\t{seq}\t1\n"
        if num % 2 == 0:
            ftrain.write(txt)
        else:
            ftest.write(txt)
        num += 1

    ftrain.close()
    ftest.close()
    fpos.close()
    os.chdir("..")


def ezgeno():
    """ https://github.com/ailabstw/ezGeno """
    # Modified from ezGeno/example/TFBind/run.sh
    name = "data/ezgeno"
    # 1.data prepareing
    docker_run(image_ezgeno, f""" \
        python ezGeno/preprocess/createdata.py \
               --filename {name}.train.seq \
               --neg_type dinucleotide \
               --outputprefix {name}.train
    """)
    docker_run(image_ezgeno, f""" \
        python ezGeno/preprocess/createdata.py \
               --filename {name}.test.seq \
               --outputprefix {name}.test \
               --reverse False
    """)
    # 2.run ezgeno code
    docker_run(image_ezgeno, f""" \
        python ezGeno/ezgeno/ezgeno.py \
               --trainFileList {name}.train.sequence \
               --trainLabel    {name}.train.label \
               --testFileList  {name}.test.sequence \
               --testLabel     {name}.test.label \
               --save          {name}.ezgeno.model
    """)
    # 3.visualize
    docker_run(image_ezgeno, f""" \
        python ezGeno/ezgeno/visualize.py --show_seq all \
               --load {name}.ezgeno.model \
               --data_path {name}.pos.fa \
               --data_name {name}.ezgeno \
               --target_layer_names "[2]"
    """)


if __name__ == "__main__":
    # download()
    suffix = ""
    # fastqc()
    # trimmomatic()
    suffix += ".trim"
    # bbmapFilterTile()
    suffix += ".trimtile"
    # fastqc()
    # bowtiePre()
    # bowtie()
    suffix += ".bowtie.filter.dedup"
    # macs2()
    suffix += ".macs2"
    # meme()
    # mergePeak()

    # Ezgeno
    # docker_build(image_ezgeno, "docker_ezgeno.dockerfile")
    # run("git clone https://github.com/ailabstw/ezGeno.git")
    # ezgenoPre()
    # ezgeno()
