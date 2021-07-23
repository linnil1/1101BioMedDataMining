"""
Homework3 Part 1

Author: linnil1
Command: python3 pipeline_hw.py
Result:

[Question 2] What is the file format that you just download?
Fasta
[Question 3] Run "blastn" with "-evalue 0.0001" argument, how many targets gene did we find?
303003
[Question 4] From the result of Question 3, we can find out that "gene A" might refer to "XM_011518391".
What is the "bit score" of "XM_011518391" when "evalue" = 0.0?
10949.0
[Question 5] From Question 3, how many "different" subject ID (subject acc.) did we get?
2491
[Question 6] From Question 3, what might be the "subject ID (subject acc.)" of gene Q?
XM_024447382.1
[Question 7] From Question 3, what is the gene name (query acc.) of "XM_011526256" in the file you download?
['I', 'I', 'I', 'I', 'I']
[Question 8] What is the beginning sequence of "XM_017025736" ?
GCTTGGCGGAGGCGGGGAAGGCCCGCAGGCGGCGCCTCAGCCGGGGTTGGCGCTGAGGGGAGAGGGCGGGGAAAAGGTGG
[Question 9] What is the gene function of "XM_017010807" ?
PREDICTED: Homo sapiens major histocompatibility complex, class I, E (HLA-E), transcript variant X1, mRNA
"""
import pandas as pd
from pipeline_1 import *


def getSample():
    return ["data/homework"]


def downloadHW():
    run(f"wget 'https://drive.google.com/u/0/uc?id=1E-sHHINtLvgMGstrJJ3PT-1MBaSOrgUh&export=download' "
        f"-O {getSample()[0]}.fa")


def blastRun():
    for name in getSample():
        # Blast default output
        docker_run(image_blast,
                   f'blastn -task blastn -query {name}.fa -db {blast_ref} '
                   f'-evalue 0.0001 -num_threads {thread} -outfmt 6 '
                   f'-out {name}.blastn.txt')


def determine_fastq(f):
    next(f)
    next(f)
    q = next(f)
    if q.strip() == "+":
        print("FastQ")
    else:
        print("Fasta")


def answerQuestion():
    # Read blast data
    df = pd.read_csv(open(getSample()[0] + ".blastn.txt"),
                     sep='\t',
                     names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch',
                            'gapopen', 'qstart', 'qend', 'sstart', 'send',
                            'evalue', 'bitscore'])

    print("[Question 2] What is the file format that you just download?")
    with open(getSample()[0] + ".fa") as f:
        determine_fastq(f)

    print('[Question 3] Run "blastn" with "-evalue 0.0001" argument, '
          'how many targets gene did we find?')
    print(len(df))

    print('[Question 4] From the result of Question 3, '
          'we can find out that "gene A" might refer to "XM_011518391".\n'
          'What is the "bit score" of "XM_011518391" when "evalue" = 0.0?')
    df3 = df[(df['qseqid'] == "A") &
             (df['sseqid'].str.startswith("XM_011518391"))]
    print(df3.iloc[(df3['evalue'] - 0).abs().argsort()[0]]['bitscore'])

    print('[Question 5] From Question 3, '
          'how many "different" subject ID (subject acc.) did we get?')
    print(len(set(df['sseqid'])))

    print('[Question 6] From Question 3, '
          'what might be the "subject ID (subject acc.)" of gene Q?')
    df6 = df[(df['qseqid'] == 'Q')]
    print(df6.iloc[df6['bitscore'].argmax()]['sseqid'])

    print('[Question 7] From Question 3, '
          'what is possible gene (query acc.) of "XM_011526256"?')
    print(df[df['sseqid'].str.startswith("XM_011526256")]
          .sort_values("evalue")['qseqid'].tolist())

    print('[Question 8] What is the beginning sequence of "XM_017025736" ?')
    with open(ref) as f:
        print_seq = False
        for line in f:
            if print_seq:
                print(line)
                print_seq = False
            if ">" == line[0]:
                print_seq = "XM_017025736" in line

    print('[Question 9] What is the gene function of "XM_017010807" ?')
    with open(ref) as f:
        for line in f:
            if "XM_017010807" in line:
                print(line.split(" ", 1)[1])


if __name__ == "__main__":
    download()  # download same thing as pipeline_1
    downloadHW()
    blastPre()
    blastRun()
    answerQuestion()
