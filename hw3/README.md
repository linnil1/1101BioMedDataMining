# Class3 and HW3

## Class3

I rewrite the pipeline in class3 by python + docker

* `pipeline_1.py` `pipeline_2.py`

Reference

* class3 https://rnabio.org/module-01-inputs/0001/05/01/RNAseq_Data/
* galaxy deseq2 code https://github.com/galaxyproject/tools-iuc/blob/master/tools/deseq2/deseq2.R


## HW3

Homework pipeline and code:

All script are written in Python except docker executing

* `pipeline_hw3_1.py` `pipeline_hw3_2.py`


## Result

Class pipeline
```
data
├── BLAST_sample_file.blastn.1.1.all_seqs.fa
├── BLAST_sample_file.blastn.1.1.txt
├── BLAST_sample_file.blastn.1.txt
├── BLAST_sample_file.blastn.2.txt
├── BLAST_sample_file.blastn.3.txt
├── BLAST_sample_file.fa
├── e2t.ctab
├── e_data.ctab
├── fastqc
│   ├── hcc1395_normal_rep1_r1.clean_fastqc.html
│   ├── hcc1395_normal_rep1_r1.clean_fastqc.zip
│   ├── hcc1395_normal_rep1_r1_fastqc.html
│   ├── hcc1395_normal_rep1_r1_fastqc.zip
│   ├── hcc1395_normal_rep1_r2.clean_fastqc.html
│   ├── hcc1395_normal_rep1_r2.clean_fastqc.zip
│   ├── hcc1395_normal_rep1_r2_fastqc.html
│   ├── hcc1395_normal_rep1_r2_fastqc.zip
│   ├── hcc1395_normal_rep2_r1.clean_fastqc.html
│   ├── hcc1395_normal_rep2_r1.clean_fastqc.zip
│   ├── hcc1395_normal_rep2_r1_fastqc.html
│   ├── hcc1395_normal_rep2_r1_fastqc.zip
│   ├── hcc1395_normal_rep2_r2.clean_fastqc.html
│   ├── hcc1395_normal_rep2_r2.clean_fastqc.zip
│   ├── hcc1395_normal_rep2_r2_fastqc.html
│   ├── hcc1395_normal_rep2_r2_fastqc.zip
│   ├── hcc1395_normal_rep3_r1.clean_fastqc.html
│   ├── hcc1395_normal_rep3_r1.clean_fastqc.zip
│   ├── hcc1395_normal_rep3_r1_fastqc.html
│   ├── hcc1395_normal_rep3_r1_fastqc.zip
│   ├── hcc1395_normal_rep3_r2.clean_fastqc.html
│   ├── hcc1395_normal_rep3_r2.clean_fastqc.zip
│   ├── hcc1395_normal_rep3_r2_fastqc.html
│   ├── hcc1395_normal_rep3_r2_fastqc.zip
│   ├── hcc1395_tumor_rep1_r1.clean_fastqc.html
│   ├── hcc1395_tumor_rep1_r1.clean_fastqc.zip
│   ├── hcc1395_tumor_rep1_r1_fastqc.html
│   ├── hcc1395_tumor_rep1_r1_fastqc.zip
│   ├── hcc1395_tumor_rep1_r2.clean_fastqc.html
│   ├── hcc1395_tumor_rep1_r2.clean_fastqc.zip
│   ├── hcc1395_tumor_rep1_r2_fastqc.html
│   ├── hcc1395_tumor_rep1_r2_fastqc.zip
│   ├── hcc1395_tumor_rep2_r1.clean_fastqc.html
│   ├── hcc1395_tumor_rep2_r1.clean_fastqc.zip
│   ├── hcc1395_tumor_rep2_r1_fastqc.html
│   ├── hcc1395_tumor_rep2_r1_fastqc.zip
│   ├── hcc1395_tumor_rep2_r2.clean_fastqc.html
│   ├── hcc1395_tumor_rep2_r2.clean_fastqc.zip
│   ├── hcc1395_tumor_rep2_r2_fastqc.html
│   ├── hcc1395_tumor_rep2_r2_fastqc.zip
│   ├── hcc1395_tumor_rep3_r1.clean_fastqc.html
│   ├── hcc1395_tumor_rep3_r1.clean_fastqc.zip
│   ├── hcc1395_tumor_rep3_r1_fastqc.html
│   ├── hcc1395_tumor_rep3_r1_fastqc.zip
│   ├── hcc1395_tumor_rep3_r2.clean_fastqc.html
│   ├── hcc1395_tumor_rep3_r2.clean_fastqc.zip
│   ├── hcc1395_tumor_rep3_r2_fastqc.html
│   └── hcc1395_tumor_rep3_r2_fastqc.zip
├── GRCh38_latest_genomic.blast.nhr
├── GRCh38_latest_genomic.blast.nin
├── GRCh38_latest_genomic.blast.nog
├── GRCh38_latest_genomic.blast.nsd
├── GRCh38_latest_genomic.blast.nsi
├── GRCh38_latest_genomic.blast.nsq
├── GRCh38_latest_genomic.fna
├── GRCh38_latest_genomic.fna.gz
├── GRCh38_latest_genomic.gff
├── GRCh38_latest_rna.blast.nhr
├── GRCh38_latest_rna.blast.nin
├── GRCh38_latest_rna.blast.nog
├── GRCh38_latest_rna.blast.nsd
├── GRCh38_latest_rna.blast.nsi
├── GRCh38_latest_rna.blast.nsq
├── GRCh38_latest_rna.fna
├── GRCh38_latest_rna.fna.NM_007297.4.fa
├── hcc1395_normal_rep1.clean.hisat.bam
├── hcc1395_normal_rep1.clean.hisat.sam
├── hcc1395_normal_rep1.clean.hisat.stringtie.gff
├── hcc1395_normal_rep1.clean.hisat.stringtie.merge.gff
├── hcc1395_normal_rep1_r1.clean.fastq.gz
├── hcc1395_normal_rep1_r1.fastq.gz
├── hcc1395_normal_rep1_r1.unpair.fastq.gz
├── hcc1395_normal_rep1_r2.clean.fastq.gz
├── hcc1395_normal_rep1_r2.fastq.gz
├── hcc1395_normal_rep1_r2.unpair.fastq.gz
├── hcc1395_normal_rep2.clean.hisat.bam
├── hcc1395_normal_rep2.clean.hisat.sam
├── hcc1395_normal_rep2.clean.hisat.stringtie.gff
├── hcc1395_normal_rep2.clean.hisat.stringtie.merge.gff
├── hcc1395_normal_rep2_r1.clean.fastq.gz
├── hcc1395_normal_rep2_r1.fastq.gz
├── hcc1395_normal_rep2_r1.unpair.fastq.gz
├── hcc1395_normal_rep2_r2.clean.fastq.gz
├── hcc1395_normal_rep2_r2.fastq.gz
├── hcc1395_normal_rep2_r2.unpair.fastq.gz
├── hcc1395_normal_rep3.clean.hisat.bam
├── hcc1395_normal_rep3.clean.hisat.sam
├── hcc1395_normal_rep3.clean.hisat.stringtie.gff
├── hcc1395_normal_rep3.clean.hisat.stringtie.merge.gff
├── hcc1395_normal_rep3_r1.clean.fastq.gz
├── hcc1395_normal_rep3_r1.fastq.gz
├── hcc1395_normal_rep3_r1.unpair.fastq.gz
├── hcc1395_normal_rep3_r2.clean.fastq.gz
├── hcc1395_normal_rep3_r2.fastq.gz
├── hcc1395_normal_rep3_r2.unpair.fastq.gz
├── hcc1395_tumor_rep1.clean.hisat.bam
├── hcc1395_tumor_rep1.clean.hisat.sam
├── hcc1395_tumor_rep1.clean.hisat.stringtie.gff
├── hcc1395_tumor_rep1.clean.hisat.stringtie.merge.gff
├── hcc1395_tumor_rep1_r1.clean.fastq.gz
├── hcc1395_tumor_rep1_r1.fastq.gz
├── hcc1395_tumor_rep1_r1.unpair.fastq.gz
├── hcc1395_tumor_rep1_r2.clean.fastq.gz
├── hcc1395_tumor_rep1_r2.fastq.gz
├── hcc1395_tumor_rep1_r2.unpair.fastq.gz
├── hcc1395_tumor_rep2.clean.hisat.bam
├── hcc1395_tumor_rep2.clean.hisat.sam
├── hcc1395_tumor_rep2.clean.hisat.stringtie.gff
├── hcc1395_tumor_rep2.clean.hisat.stringtie.merge.gff
├── hcc1395_tumor_rep2_r1.clean.fastq.gz
├── hcc1395_tumor_rep2_r1.fastq.gz
├── hcc1395_tumor_rep2_r1.unpair.fastq.gz
├── hcc1395_tumor_rep2_r2.clean.fastq.gz
├── hcc1395_tumor_rep2_r2.fastq.gz
├── hcc1395_tumor_rep2_r2.unpair.fastq.gz
├── hcc1395_tumor_rep3.clean.hisat.bam
├── hcc1395_tumor_rep3.clean.hisat.sam
├── hcc1395_tumor_rep3.clean.hisat.stringtie.gff
├── hcc1395_tumor_rep3.clean.hisat.stringtie.merge.gff
├── hcc1395_tumor_rep3_r1.clean.fastq.gz
├── hcc1395_tumor_rep3_r1.fastq.gz
├── hcc1395_tumor_rep3_r1.unpair.fastq.gz
├── hcc1395_tumor_rep3_r2.clean.fastq.gz
├── hcc1395_tumor_rep3_r2.fastq.gz
├── hcc1395_tumor_rep3_r2.unpair.fastq.gz
├── homework.blastn.txt
├── homework.fa
├── i2t.ctab
├── i_data.ctab
├── merge.list
├── merge.stringtie.compare
├── merge.stringtie.compare.annotated.gtf
├── merge.stringtie.compare.loci
├── merge.stringtie.compare.merge.stringtie.gff.refmap
├── merge.stringtie.compare.merge.stringtie.gff.tmap
├── merge.stringtie.compare.tracking
├── merge.stringtie.gff
├── merge.stringtie.result.gene.csv
├── merge.stringtie.result.tx.csv
├── merge.stringtie.result.tx.deseq.csv
├── merge.stringtie.result.tx.deseq.pdf
├── practical.tar
└── t_data.ctab
```

Homework3 Part 1

```
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
```

Homework3 Part 2

```
[Question 2] What is the file format that you download from "http://genomedata.org/rnaseq-tutorial/practical.tar"?
FastQ
[Question 3] What adaptor sequences that we use in Trimmomatic? Please click on two sequences.
>PrefixPE/1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
[Question 4] After running Trimmomatic, what is the closest "first base" "mean" that shows in "FastQC_data" of hcc1395_normal_rep2_r1_clean_paired.fastq
  #Base       Mean  Median  Lower Quartile  Upper Quartile  10th Percentile  90th Percentile
  0     1  30.900412    32.0            32.0            32.0             27.0             32.0
  1     2  31.509489    32.0            32.0            32.0             32.0             32.0
  2     3  35.853593    37.0            37.0            37.0             32.0             37.0
  3     4  36.370096    37.0            37.0            37.0             37.0             37.0
  4     5  36.560014    37.0            37.0            37.0             37.0             37.0
[Question 5] After processing "stringtie --merge", all the "gene_name and ref_gene_id" are in NC_000001.11 "except"?
sys:1: DtypeWarning: Columns (5) have mixed types.Specify dtype option on import or set low_memory=False.
PARK7 False
ENO1 True
MIR398 False
RPL22 False
[Question 7] After processing DESeq2, you can get "gene_diff.csv". What is the closest "padj" number of "rna-NM_000362.5" ?
2.67085238337022e-13
[Question 8] Please search "rna-NM_005318.4" gene in your DESeq2 output file (gene_diff.csv). Which part tissue express more "rna-NM_005318.4" ?
tumor
[Question 9] Which gene express more in normal than tumor
Row.names         rna-XM_017029019.2
log2FoldChange              -4.86086
```
