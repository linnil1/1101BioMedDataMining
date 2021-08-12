# Week6 Lecture and Homework

TOC

* ChIP-Seq Analysis
* Use ezGeno to find motif from fasta

Both pipeline written in 

`python pipeline_chip.py`

## ChIP-Seq Analysis

Reference pipeline https://www.pnas.org/content/118/20/e2026754118

Lecture: https://hackmd.io/TJ7ree27SveRzdM6gEvlQA?view

Discovered Logo

![logo1](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw6/data/ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.meme/meme_out/logo1.png)
![logo_rc1](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw6/data/ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.meme/meme_out/logo_rc1.png)

## ezGeno

If you don't have GPU mechine, you need to modified some code after git clone

Training Result
```
test auc: 0.930272
Epoch 30
Training acc: 92.50%
Train AUC score: 0.9808
Epoch 30
Training acc: 93.00%
Train AUC score: 0.9968
Test AUC score: 0.9309

test auc: 0.930912
Test AUC score: 0.9309
```

Logo
```
>seq_320_20_31_tensor([[0.5869]], grad_fn=<AddmmBackward>)
TCCGTTGTGGTT
```

[ezGeno Visualization](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw6/data/ezgeno.ezgeno_seq_pos_heatmap.pdf)



## Result

```
data/
├── ENCFF000YND.fastq.gz
├── ENCFF000YND.trim.fastq.gz
├── ENCFF000YND.trim.trimtile.fastq.gz
├── ENCFF000YND.trim.trimtile.bowtie.sam
├── ENCFF000YND.trim.trimtile.bowtie.filter.bam
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.bam
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.bam.bai
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2_model.r
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2_peaks.narrowPeak
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.peaks.sort.narrowPeak
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2_peaks.xls
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2_summits.bed
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.bed
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.bed
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.bed
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.fa
├── ENCFF000YND.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.meme
│   ├── background
│   ├── ...
│   ├── combined.meme
│   ├── meme-chip.html
│   ├── meme_out
│   │   ├── logo1.eps
│   │   ├── logo1.png
│   │   ├── meme.html
│   │   ├── meme.txt
│   │   └── meme.xml
│   ├── motif_alignment.txt
│   ├── progress_log.txt
│   └── summary.tsv
├── ENCFF000YNF.fastq.gz
├── ENCFF000YNF.trim.fastq.gz
├── ENCFF000YNF.trim.trimtile.fastq.gz
├── ENCFF000YNF.trim.trimtile.bowtie.sam
├── ENCFF000YNF.trim.trimtile.bowtie.filter.bam
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.bam
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.bam.bai
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2_model.r
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2_peaks.narrowPeak
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.peaks.sort.narrowPeak
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2_peaks.xls
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2_summits.bed
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.bed
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.bed
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.bed
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.fa
├── ENCFF000YNF.trim.trimtile.bowtie.filter.dedup.macs2.summit.extend.excluded.top.peaks.meme
│   ├── background
│   ├── combined.meme
│   ├── meme-chip.html
│   ├── meme_out
│   │   ├── logo1.eps
│   │   ├── logo1.png
│   │   ├── meme.html
│   │   ├── meme.txt
│   │   └── meme.xml
│   ├── motif_alignment.txt
│   ├── progress_log.txt
│   └── summary.tsv
├── ENCFF000YN.merge.idr
├── ENCFF000YN.merge.idr.log
├── ENCFF000YN.merge.idr.png
├── ENCFF000YQC.fastq.gz
├── ENCFF000YQC.trim.fastq.gz
├── ENCFF000YQC.trim.trimtile.fastq.gz -> ENCFF000YQC.trim.fastq.gz
├── ENCFF000YQC.trim.trimtile.bowtie.sam
├── ENCFF000YQC.trim.trimtile.bowtie.filter.bam
├── ENCFF000YQC.trim.trimtile.bowtie.filter.dedup.bam
├── ENCFF000YQC.trim.trimtile.bowtie.filter.dedup.bam.bai
├── ENCFF023CZC.bed.gz
├── ezgeno.ezgeno_grad_cam.csv
├── ezgeno.ezgeno.model
├── ezgeno.ezgeno_seq_pos_heatmap.pdf
├── ezgeno.ezgeno_sequence_logo.fa
├── ezgeno.fa
├── ezgeno.pos.fa
├── ezgeno.test.label
├── ezgeno.test.seq
├── ezgeno.test.sequence
├── ezgeno.train.label
├── ezgeno.train.seq
├── ezgeno.train.sequence
├── fastqc
│   ├── ENCFF000YND_fastqc.html
│   ├── ENCFF000YND_fastqc.zip
│   └── ...
├── Homo_sapiens.GRCh38.dna.primary_assembly.fa
├── Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai
├── Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
├── Homo_sapiens.GRCh38.dna.primary_assembly.1.bt2
├── Homo_sapiens.GRCh38.dna.primary_assembly.2.bt2
├── Homo_sapiens.GRCh38.dna.primary_assembly.3.bt2
├── Homo_sapiens.GRCh38.dna.primary_assembly.4.bt2
├── Homo_sapiens.GRCh38.dna.primary_assembly.rev.1.bt2
├── Homo_sapiens.GRCh38.dna.primary_assembly.rev.2.bt2
└── TruSeq3-SE.fa
```

## Homework6

See hw6 function in `pipeline_chip.py`

```
Peak per chromsome:
1             567
10            234
11            249
12            241
13             68
14             84
15            140
16            167
17            185
18             92
19            118
2             389
20             98
21             64
22            109
3             300
4             190
5             249
6             370
7             249
8             225
9             173
GL000205.2      1
GL000219.1      1
KI270438.1      5
KI270709.1      1
KI270733.1      2
MT             10
X             118

Num of Peak IDR < 0.05:  2485
```

[data/ENCFF000YN.merge.idr.count.csv](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw6/data/ENCFF000YN.merge.idr.count.csv)
