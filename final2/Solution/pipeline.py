import sys
import re
from collections import defaultdict, Counter
from pprint import pprint


def clivarRead(file_clinvarvcf, target_chr="17", target_pos=[41194312, 41279381]):
    """
    Read clinvar.vcf

    Returns:
      list of CLNSIG
    """
    tot_clivar = 0
    clivar = []
    db_check = set()
    with open(file_clinvarvcf) as vcf:
        for i in vcf:
            # comment
            if i.startswith("#"):
                continue
            # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
            # 1	861332	1019397	G	A	.	.	ALLELEID=1003021;CLNDISDB=MedGen:CN517202;CLNDN=not_provided;CLNHGVS=NC_000001.10:g.861332G>A;CLNREVSTAT=criteria_provided,_single_submitter;CLNSIG=Uncertain_significance;CLNVC=single_nucleotide_variant;CLNVCSO=SO:0001483;GENEINFO=SAMD11:148398;MC=SO:0001583|missense_variant;ORIGIN=1
            # 1	865628	789256	G	A	.	.	AF_ESP=0.00347;AF_EXAC=0.00622;AF_TGP=0.00280;ALLELEID=707587;CLNDISDB=MedGen:CN517202;CLNDN=not_provided;CLNHGVS=NC_000001.10:g.865628G>A;CLNREVSTAT=criteria_provided,_single_submitter;CLNSIG=Likely_benign;CLNVC=single_nucleotide_variant;CLNVCSO=SO:0001483;GENEINFO=SAMD11:148398;MC=SO:0001583|missense_variant;ORIGIN=1;RS=41285790
            cols = i.strip().split("\t")

            # check is inside region
            if cols[0] != target_chr:
                continue
            if not (
                target_pos[0] <= int(cols[1]) <= target_pos[1]
                # deletion
                or target_pos[0] <= int(cols[1]) + len(cols[3]) - 1 <= target_pos[1]
            ):
                continue

            # OK
            tot_clivar += 1
            # CLNSIG
            sig = re.findall(r"CLNSIG=([\w/,]+)", cols[-1])
            if not sig:
                sig = "None"
            else:
                sig = sig[0]
            clivar.append(sig)

            # double check
            variant = (cols[0], cols[1], cols[2], cols[3])
            assert variant not in db_check
            db_check.add(variant)

    return tot_clivar, clivar


def cutRegion(region):
    chrom, pos = region.split(":")
    chrom = chrom[3:]
    pos = [int(i) for i in pos.split('-')]
    return chrom, pos


if __name__ == "__main__":
    # program.py clinvar.vcf chr17:41194312-41279381
    chrom, pos = cutRegion(sys.argv[2])
    tot, clivar = clivarRead(sys.argv[1], target_chr=chrom, target_pos=pos)
    print("Query:", sys.argv[2])
    print("  Total:", tot, "variants")
    print("  Catelog:")
    for k, v in sorted(Counter(clivar).items(), key=lambda i: i[0].lower()):
        print(f"    {k:70s} {v:8d}")
