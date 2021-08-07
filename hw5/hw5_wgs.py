import os
import time
import gzip
import pandas as pd
from tqdm import tqdm
from utils import run, googleDownload


name = "data/SRR702068.hg38_multianno.vcf"


def download():
    run("mkdir -p data")
    if not os.path.exists(f"{name}.gz"):
        googleDownload("1POAO4Vi6-Luz2SXKhNhERFaV2KbL17Sv")
        print("File downloaded?", os.path.exists(f"{name}.gz"))


def countPass():
    count = {
        'SNP': {
            'Total': 0,
            'Pass': 0,
        },
        'INDEL': {
            'Total': 0,
            'Pass': 0,
        }
    }

    with gzip.open(f"{name}.gz", "rt") as f:
        for line in tqdm(f):
            # columns header
            # #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  SM_SRR702068
            if line.startswith("#"):
                continue
            line_sp = line.split("\t")

            # count pass/total
            genotype = 'SNP' if len(line_sp[3]) == len(line_sp[4]) == 1 else 'INDEL'
            count[genotype]['Total'] += 1
            if line_sp[6] == "PASS":
                count[genotype]['Pass'] += 1
            # More Check
            # if genotype == "SNP":
            #     if line_sp[3] not in "ATCG":
            #         print(line_sp[:7])
            #     if line_sp[4] not in "ATCG":
            #         print(line_sp[:7])
            # Found:
            #   A/*
            # Check this reference:
            #   https://gatk.broadinstitute.org/hc/en-us/articles/360035531912-Spanning-or-overlapping-deletions-allele-

    return count


download()
count = countPass()
data = pd.DataFrame(count).T
print(data)
data.to_csv(f"{name}.statistics.csv")
