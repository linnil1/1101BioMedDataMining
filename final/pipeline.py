import re
import os
import time
from collections import defaultdict, Counter
from pprint import pprint


def run(cmd):
    print(f'[{time.strftime("%c")}] ' + cmd)
    os.system(cmd)


def docker_run(image, cmd, other=""):
    run(f"docker run -it --rm -v $PWD:/app "
        f"--security-opt label=disable {other} "
        f"-w /app {image} {cmd}")


def googleDownload(id):
    docker_run('docker.io/library/python:3.9',
               'bash -c "pip install gdown && '
               f'gdown --id {id}')


def download():
    """
    Download needed data
    https://drive.google.com/drive/u/2/folders/1dzZefJOKvp0o0UZhXgJ2H5ETYZDulmu_
    """
    googleDownload("1N-OM06pTulxdcNP0fc6bvCJNoZoGwqTy")
    googleDownload("1jA_vQAPv6YeSxVmTL38mgNMMW_06Uw7o")
    googleDownload("1_-w5GDMRPDF75OfMBHuGLRcpWft5MP-I")
    googleDownload("10cpTT83pKJvsWbQe9Fwava7BBXXRfcJT")


def reverseCom(arr):
    m = {
        'A': 'T',
        'T': 'A',
        'G': 'C',
        'C': 'G',
    }
    return "".join(map(lambda i: m[i], arr))


def readSample(file_chipcsv):
    """
    Read rows in sample (chip.csv)

    Returns: a list of sample_variant
      [[chrpos, ref, alt], ...]
    """
    non_bottop = 0
    tot = 0
    ids = []
    with open(file_chipcsv) as sample_text:
        for i in sample_text:
            if "IlmnID" in i:
                break
        for i in sample_text:
            # IlmnID,Name,IlmnStrand,SNP,AddressA_ID,AlleleA_ProbeSeq,AddressB_ID,AlleleB_ProbeSeq,GenomeBuild,Chr,MapInfo,Ploidy,Species,Source,SourceVersion,SourceStrand,SourceSeq,TopGenomicSeq,BeadSetID,Exp_Clusters,Intensity_Only,RefStrand

            # 1:103380393-0_B_R_2346041316,1:103380393,BOT,[T/C],0009663149,AATAAACTTTTATGCAAAACTTGTAAGATAACTCTTCTTTCCTTCTTCTT,,,37,1,103380393,diploid,Homo sapiens,1000genomes,0,TOP,GCTTCCCCTTTCTCTCCTCTTTCTCCTTTGGGACCCTAAACAATGTTAAAAAAAAAAAAA[A/G]AAGAAGAAGGAAAGAAGAGTTATCTTACAAGTTTTGCATAAAAGTTTATTAACCTTGGCA,GCTTCCCCTTTCTCTCCTCTTTCTCCTTTGGGACCCTAAACAATGTTAAAAAAAAAAAAA[A/G]AAGAAGAAGGAAAGAAGAGTTATCTTACAAGTTTTGCATAAAAGTTTATTAACCTTGGCA,1895,3,0,-
            # In the last of file
            if "[Controls]" in i:
                break
            cols = i.strip().split(",")
            tot += 1
            # name, snp, ilumnstrand, refstrand
            info = (cols[1], cols[3], cols[2], cols[-1])
            if info[2] not in ["BOT", "TOP"]:
                non_bottop += 1
                continue

            a1, a2 = info[1][1:-1].split("/")
            if cols[-1] == "-":
                id = (cols[1], reverseCom(a1), reverseCom(a2))
            else:
                id = (cols[1], a1, a2)
            ids.append(id)

    print("Total row in sample (chip.csv)", tot)
    print("  not bottop", non_bottop)
    print("  bot or top", len(ids), "( unique", len(set(ids)), ")")
    return ids


def rsidRead(file_chiprsid):
    """
    Read chip_rsid.txt, then we can
    map the chr+pos info in chip.txt to a rsid

    Returns:
      {chrpos: rsid}
    """
    m = {}
    no_rsid = 0
    for i in open(file_chiprsid):
        # Name	RsID
        # 1:103380393	rs577266494
        if "Name" not in i:
            name, rsid = i.strip().split("\t")
            assert name not in m
            if rsid == ".":
                no_rsid += 1
            else:
                m[name] = rsid
    print("Total row in chip_rsid", no_rsid + len(m))
    print("  alleleID without rsid", no_rsid)
    print("  alleleID with rsid", len(m))
    return m


def name2rsid(rsid_map, variants):
    """
    Add rsid column(chip_rsid) in each variants in chip.csv

    Parameters:
      rsid_map: come from rsidRead()
      variants: a list of sample_variant from readSample()

    Returns:
      [sample_variant]: sample_variant with additional column: rsid
    """
    no_include = 0
    ids = []
    for v in variants:
        if v[0] not in rsid_map:
            no_include += 1
        else:
            ids.append((*v, rsid_map[v[0]]))
    print("    sample no rsid mapping from chip_rsid", no_include)
    print("    sample rsid mapping", len(ids))
    return ids


def alleleidRead(file_clinvar_rsid):
    """
    Read the mapping from alleleid(clinvar) to rsid

    Returns:
      {alleleid: rsid}
    """
    m = {}
    tot_allele = 9
    no_rsid = 0
    dup_map = 0
    for i in open(file_clinvar_rsid):
        if "AlleleID" not in i:
            tot_allele += 1
            alleleid, db, id, updated = i.strip().split("\t")
            rsid = "rs" + id
            # 15104   dbSNP   121918057       Oct 19, 2015
            # 15105   dbSNP   121918057       Oct 19, 2015
            try:
                int(id)
            except:
                no_rsid += 1
                continue
            # assert alleleid not in m
            # print(i)
            if alleleid in m:
                dup_map += 1
            else:
                m[alleleid] = rsid
    print("Total row in clinvar_rsid.txt", tot_allele)
    print("  no rsid", no_rsid)
    print("  duplicated", dup_map)
    print("  success records", len(m))
    return m


def clivarRead(file_clinvarvcf):
    """
    Read clinvar.vcf

    Returns: a list of clinvar_element
      [[chrpos, ref, alt, alleleid, rsid, significant], ...]
    """
    tot_clivar = 0
    no_allele = 0
    no_rsid = 0
    no_sig = 0
    num_dup = 0
    clivar = []
    with open(file_clinvarvcf) as vcf:
        for i in vcf:
            if not i.startswith("#"):
                break
        for i in vcf:
            tot_clivar += 1
            cols = i.strip().split("\t")
            # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
            # 1	861332	1019397	G	A	.	.	ALLELEID=1003021;CLNDISDB=MedGen:CN517202;CLNDN=not_provided;CLNHGVS=NC_000001.10:g.861332G>A;CLNREVSTAT=criteria_provided,_single_submitter;CLNSIG=Uncertain_significance;CLNVC=single_nucleotide_variant;CLNVCSO=SO:0001483;GENEINFO=SAMD11:148398;MC=SO:0001583|missense_variant;ORIGIN=1
            # 1	865628	789256	G	A	.	.	AF_ESP=0.00347;AF_EXAC=0.00622;AF_TGP=0.00280;ALLELEID=707587;CLNDISDB=MedGen:CN517202;CLNDN=not_provided;CLNHGVS=NC_000001.10:g.865628G>A;CLNREVSTAT=criteria_provided,_single_submitter;CLNSIG=Likely_benign;CLNVC=single_nucleotide_variant;CLNVCSO=SO:0001483;GENEINFO=SAMD11:148398;MC=SO:0001583|missense_variant;ORIGIN=1;RS=41285790
            sig = re.findall(r"CLNSIG=(.*?);", cols[-1])
            if not sig:
                no_sig += 1
                continue
            else:
                sig = sig[0]

            allele = re.findall(r"ALLELEID=(\w+)", cols[-1])
            if not allele:
                no_allele += 1
                continue
            else:
                allele = allele[0]

            rs = re.findall(r"RS=(\w+)", cols[-1])
            if rs and rs[0]:
                rs = rs[0]
            else:
                no_rsid += 1
                rs = None
                continue

            # chrpos ref alt allele rs annotation
            chrpos = cols[0] + ":" + cols[1]
            clivar.append([chrpos, cols[3], cols[4], allele, rs, sig])
    print("Total row in Clinvar.csv", tot_clivar)
    print("  no Annotation", no_sig)
    print("    no alleleid", no_allele)
    print("      no rsid", no_rsid)
    print("        success mapped", len(clivar), "unique:", len(set([i[3] for i in clivar])))
    return clivar


def addRsidOnClinvar(clivar_list, alleleid_map):
    """
    Add additional rsid column in clinvar.vcf

    Parameters:
      clivar_list: a list of clinvar_element from clivarRead()
      alleleid_map: from alleleidRead()

    Returns:
      [clinvar_element_rsid]: a list of clivar_element with additional rsid column
    """
    no_allele_map = 0
    no_allele_not_map = 0
    for i in clivar_list:
        if i[3] in alleleid_map:
            no_allele_map += 1
            i.append(alleleid_map[i[3]])
        else:
            no_allele_not_map += 1

    print("          no rsid mapping according clinvar_rsid.txt", no_allele_not_map)
    print("          success rsid mapped", no_allele_map)

    no_rsid_iconsis = 0
    for i in clivar_list:
        if "rs" + i[4] != i[-1]:
            no_rsid_iconsis += 1
            # print("rsid inconsistent", i)
    print("          (rsid inconsistent)", no_rsid_iconsis)
    return clivar_list


def findRefalt(ref, alt, clivars):
    """
    Find the element in the list with same ref/alt or alt/ref from given ref alt

    Parameters:
      ref: str
      alt: str
      clivars: a list of clinvar_element

    Return:
      clinvar_element
    """
    for cv in clivars:
        if ref == cv[1] and alt == cv[2]:
            return cv
        if ref == cv[2] and alt == cv[1]:
            return cv
    return None


def mapClinvar(clivar_map, variants_rsid):
    """
    Map the variants in sample to clinvar record

    Parameters:
      clivar_map: A dict with key=rsid value=clinvar_element_rsid
      variants_rsid: A list of sample_variant_rsid

    Returns:
      clinvar_element_rsid
    """
    no_clinvar_rsid = 0
    no_clinvar_alt = 0
    mapped_clivars = []

    for i in variants_rsid:
        if i[3] not in clivar_map:
            no_clinvar_rsid += 1
            continue
        cv = findRefalt(i[1], i[2], clivar_map[i[3]])
        if not cv:
            no_clinvar_alt += 1
            continue
        mapped_clivars.append(cv)

    print("      sample cannot mapped by rsid to clinvar", no_clinvar_rsid)
    print("      sample cannot find ref/alt with rsid", no_clinvar_alt)
    print("      sample found clinvar record in rsid", len(mapped_clivars))
    return mapped_clivars


def countSignificant(clivar_list):
    """
    Count the occourance of variant significnats

    Parameters:
      [clinvar_element_rsid]

    Reutnrs:
      dict
    """
    count = Counter([i[5].split(",")[0] for i in clivar_list])
    count_header = ['Benign', 'Benign/Likely_benign', 'Likely_benign',
                    'Likely_pathogenic', 'Pathogenic/Likely_pathogenic', 'Pathogenic',
                    'Uncertain_significance', 'drug_response', 'not_provided']
    count = {i: j for i, j in count.items() if i in count_header}
    pprint(count)
    print("    Total included significant:", sum(count.values()))
    return count


def tarSolution():
    run("mkdir -p Solution")
    run("cp run.sh Solution")
    run("cp pipeline.py Solution")
    run("tar vcf Solution.tar Solution")
    run("rm -r Solution")


if __name__ == "__main__":
    # download()
    file_clinvar_rsid = "clinvar_rsid.txt"
    file_clinvarvcf = "clinvar.vcf"
    file_chipcsv = "chip.csv"
    file_chiprsid = "chip_rsid.txt"
    file_output = "ans1.csv"

    clivar_list = clivarRead(file_clinvarvcf)
    alleleid_map = alleleidRead(file_clinvar_rsid)
    clivar_list = addRsidOnClinvar(clivar_list, alleleid_map)
    clivar_map = defaultdict(list)
    # pprint(countSignificant(clivar_list))
    for i in clivar_list:
        clivar_map[i[6]].append(i)

    rsid_map = rsidRead(file_chiprsid)
    variants = readSample(file_chipcsv)
    variants_rsid = name2rsid(rsid_map, variants)
    mapped_clivar = mapClinvar(clivar_map, variants_rsid)
    count = countSignificant(mapped_clivar)

    with open(file_output, "w") as f:
        for i, j in count.items():
            print(f"{i},{j}", file=f)
    ans1 = {
        'Benign': 7221,
        'Benign/Likely_benign': 2915,
        'Likely_benign': 2172,
        'Likely_pathogenic': 3650,
        'Pathogenic/Likely_pathogenic': 3239,
        'Pathogenic': 17204,
        'Uncertain_significance': 3367,
        'drug_response': 267,
        'not_provided': 367,
    }
    print("real answer")
    pprint(ans1)
