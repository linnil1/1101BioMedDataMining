import os
import time

# init data
os.makedirs("data/", exist_ok=True)
thread      = 20
ref         = "data/GRCh38_latest_rna.fna"
blast_ref   = "data/GRCh38_latest_rna.blast"
image_blast = "quay.io/biocontainers/blast:2.9.0--pl526he19e7b1_7"
image_blast = "quay.io/biocontainers/blast:2.12.0--pl5262h3289130_0"


def run(cmd):
    print(f'[{time.strftime("%c")}] ' + cmd)
    os.system(cmd)


def docker_run(image, cmd):
    run(f"docker run -it --rm --security-opt label=disable -v $PWD:/app "
        f"-w /app {image} {cmd}")


def download():
    run(f"wget https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_rna.fna.gz "
        f"-O {ref}.gz")
    run(f"gunzip {ref}.gz")
    run(f'wget "https://drive.google.com/u/0/uc?id=14xwvsy6Qec_qfcT6eG_n7wKqclFIOQkB&export=download" '
        f'-O "data/BLAST_sample_file.fa"')


def getSample():
    return ["data/BLAST_sample_file"]


def blastInit():
    docker_run(image_blast,
               f'time makeblastdb -dbtype nucl -parse_seqids '
               f'-in {ref} -out {blast_ref}')


def blastRun():
    for name in getSample():
        # Blast default output
        docker_run(image_blast,
                   f'blastn -task blastn -query {name}.fa -db {blast_ref} '
                   f'-evalue 0.05 -num_threads {thread} '
                   f'-out {name}.blastn.1.txt')

        # Customized output table
        docker_run(image_blast,
                   f'blastn -task blastn -query {name}.fa -db {blast_ref} '
                   f'-outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore staxids" '
                   f'-num_threads {thread} -out {name}.blastn.2.txt')

        # Get an sequence
        docker_run(image_blast,
                   f'blastdbcmd -db {blast_ref} -entry NM_007297.4 '
                   f'> {ref}.NM_007297.4.fa')

        # Get all sequence related to query
        run(f"cat {name}.blastn.2.txt | awk '{{print $2}}' | sed '1,5d;$d' "
            f"> {name}.blastn.1.1.txt")
        docker_run(image_blast,
                   f'blastdbcmd -db {blast_ref} '
                   f'-entry_batch {name}.blastn.1.1.txt '
                   f'> {name}.blastn.1.1.all_seqs.fa')

        # Connect to remote
        docker_run(image_blast,
                   f'blastn -query {ref} -db nt -remote -evalue 0.005 '
                   f'-outfmt 6 -out {name}.blastn.2.txt')


if __name__ == "__main__":
    download()
    blastInit()
    blastRun()
