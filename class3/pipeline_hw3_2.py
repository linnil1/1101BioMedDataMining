import io
import gzip
import zipfile
import pandas as pd
from pipeline_2 import *
from pipeline_hw3_1 import determine_fastq


if __name__ == "__main__":
    print('[Question 2] What is the file format that you download from '
          '"http://genomedata.org/rnaseq-tutorial/practical.tar"?')
    with gzip.open(getSample()[0] + "_r1.fastq.gz", "rt") as f:
        determine_fastq(f)

    print('[Question 3] What adaptor sequences that we use in Trimmomatic?'
          ' Please click on two sequences.')
    print(open("TruSeq3-PE.fa").read())

    print('[Question 4] After running Trimmomatic, '
          'what is the closest "first base" "mean" that shows in "FastQC_data"'
          ' of hcc1395_normal_rep2_r1_clean_paired.fastq')
    lines = []
    name = "hcc1395_normal_rep2_r1.clean"
    with zipfile.ZipFile(f"data/fastqc/{name}_fastqc.zip") as f:
        with f.open(f"{name}_fastqc/fastqc_data.txt") as f1:
            start = False
            for line in f1:
                line = line.decode()
                if start and line.startswith(">>"):
                    break
                if start:
                    lines.append(line)
                if line.startswith("#Base"):
                    start = True
                    lines.append(line)
    print(pd.read_csv(io.StringIO(''.join(lines)), sep='\t').iloc[:5])

    print('[Question 5] After processing "stringtie --merge", '
          'all the "gene_name and ref_gene_id" are in NC_000001.11 "except"?')
    gff = pd.read_csv(open(stringtie_merge + ".gff"), sep='\t',
                      skiprows=[0, 1], header=None, low_memory=False)
    gene = set(gff[gff[0] == "NC_000001.11"][8]
               .str.extract(r'gene_id "(.*?)"')[0])

    def checkInSet(gene, name):
        print(name, any(1 for i in gene if name in str(i)))

    checkInSet(gene, "PARK7")
    checkInSet(gene, "ENO1")
    checkInSet(gene, "MIR398")
    checkInSet(gene, "RPL22")

    print('[Question 7] After processing DESeq2, you can get "gene_diff.csv". '
          'What is the closest "padj" number of "rna-NM_000362.5" ?')
    deseq = pd.read_csv(stringtie_merge + ".result.tx.deseq.csv")
    deseq['log2FoldChange'] = deseq['log2FoldChange'].astype(float)
    print(float(deseq[deseq['Row.names'] == "rna-NM_000362.5"]['padj']))

    print('[Question 8] Please search "rna-NM_005318.4" gene '
          'in your DESeq2 output file (gene_diff.csv). '
          'Which part tissue express more "rna-NM_005318.4" ?')
    # note tumor vs normal =  tumor / normal
    if any(deseq[deseq['Row.names'] == "rna-NM_005318.4"]
            ['log2FoldChange'] > 0):
        print("tumor")
    else:
        print("normal")

    print('[Question 9] Which gene express more in normal than tumor')
    df9 = deseq[deseq['Row.names']
                     .isin(["rna-XM_017029019.2", "rna-NM_080430.4",
                            "rna-XM_017028814.1", "rna-NM_005318.4"])] \
               .sort_values('log2FoldChange')
    print(df9[["Row.names", "log2FoldChange"]].iloc[0])
