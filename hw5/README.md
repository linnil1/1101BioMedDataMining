# Week5: GATK and WGAS + PRS

## GATK

Variant Calling and Annotation

Not Yet

## Homework: Read GATK result

Read vcf and count pass SNPs and Indels.

``` bash
python hw5_wgs.py
```

Result stored in `data/SRR702068.hg38_multianno.vcf.statistics.csv`

```
       Total   Pass
SNP   182394 164968
INDEL  18620  17844
```

## Pipeline for Whole Genome Study(WGS)

Read the large vcf contains 1200 samples to plink

Run QC, association test and plot the result

`example_wgs.vcf.gz` is a simulated data and not available online

``` bash
python pipeline_wgs.py
```

### QC Result

``` txt
1200 samples (0 females, 0 males, 1200 ambiguous; 1200 founders) loaded from
data/example_wgs.plink.psam.
276536 variants loaded from data/example_wgs.plink.pvar.
1 binary phenotype loaded (200 cases, 1000 controls).
Calculating sample missingness rates... done.
0 samples removed due to missing genotype data (--mind).
1200 samples (0 females, 0 males, 1200 ambiguous; 1200 founders) remaining
after main filters.
200 cases and 1000 controls remaining after main filters.
Calculating allele frequencies... done.
--geno: 0 variants removed due to missing genotype data.
--hwe: 867 variants removed due to Hardy-Weinberg exact test (founders only).
27897 variants removed due to allele frequency threshold(s)
(--maf/--max-maf/--mac/--max-mac).
247772 variants remaining after main filters.
```

### File sturcture

```
data/
├── example_wgs.csv
├── example_wgs.plink.filter.assoc.csv -> example_wgs.plink.filter.assoc.PHENOTYPE.glm.logistic
├── example_wgs.plink.filter.assoc.log
├── example_wgs.plink.filter.assoc.manhattan.png
├── example_wgs.plink.filter.assoc.pgen
├── example_wgs.plink.filter.assoc.PHENOTYPE.glm.logistic
├── example_wgs.plink.filter.assoc.psam
├── example_wgs.plink.filter.assoc.pvar
├── example_wgs.plink.filter.assoc.qqplot.png
├── example_wgs.plink.filter.log
├── example_wgs.plink.filter.pgen
├── example_wgs.plink.filter.psam
├── example_wgs.plink.filter.pvar
├── example_wgs.plink.log
├── example_wgs.plink.pgen
├── example_wgs.plink.psam
├── example_wgs.plink.pvar
├── example_wgs.vcf.gz
```

### Association result

First 5 p-value allele
```
       X.CHROM       POS          ID REF ALT A1 TEST OBS_CT       OR LOG.OR._SE   Z_STAT           P
112          1   3312914 AX-75178064   T   G  T  ADD   1196 1.555830   0.111410  3.96740 7.26596e-05
22893        2  29506693 AX-11274236   A   G  A  ADD   1200 1.742940   0.133943  4.14785 3.35611e-05
22894        2  29507795 AX-13918660   G   C  G  ADD   1198 1.716710   0.131819  4.09965 4.13781e-05
29759        2 107493123 AX-11517196   C   T  T  ADD   1174 1.644320   0.124986  3.97905 6.91925e-05
38957        2 230877849 AX-11316653   T   G  G  ADD   1195 1.611360   0.115761  4.12123 3.76858e-05
39829        2 239689546 AX-11700303   T   C  T  ADD   1190 0.636032   0.116145 -3.89604 9.77768e-05
```

### plot

![ManhattanPlot](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/example_wgs.plink.filter.assoc.manhattan.png)
![QQplot](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/example_wgs.plink.filter.assoc.qqplot.png)


## Pipeline for PolyGenic Risk Score(PRS)

Download data from https://github.com/MareesAT/GWA_tutorial

Load the HapMap_3_r3_1 by Plink. (You can run QC, manhattan plot same in the above code)

Set training test ratio 4:1 from 56(control) + 56(case) samples
( i.e 45+45 for train and 11+11 for test )

Note: this is very small training set, it is expected to get bad performance. (i.e. low AUC)

Calculate PRS by

1. plink odds ratio
2. GenEpi
3. PRScs

Code: `python pipeline_prs.py`

### Directory Structure

```
data/
├── HapMap_3_r3_1.bed
├── HapMap_3_r3_1.bim
├── HapMap_3_r3_1.fam
├── HapMap_3_r3_1.plink.afreq
├── HapMap_3_r3_1.plink.geneepi
│   ├── crossGeneResult
│   │   ├── Classifier.pkl
│   │   ├── Feature.csv
│   │   ├── GenEpi_PGS_CV.png
│   │   ├── GenEpi_Prevalence_CV.png
│   │   ├── GenEpi_ROC_CV.png
│   │   └── Result.csv
│   ├── isolatedValidation
│   │   ├── GenEpi_PGS_ISO.png
│   │   ├── GenEpi_Prevalence_ISO.png
│   │   └── GenEpi_ROC_ISO.png
├── HapMap_3_r3_1.plink.pgen
├── HapMap_3_r3_1.plink.plinkprs.score.log
├── HapMap_3_r3_1.plink.plinkprs.score.roc.png
├── HapMap_3_r3_1.plink.plinkprs.score.sscore
├── HapMap_3_r3_1.plink.prscs.merge.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr10.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr11.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr12.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr13.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr14.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr15.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr16.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr17.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr18.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr19.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr1.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr20.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr21.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr22.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr2.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr3.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr4.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr5.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr6.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr7.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr8.txt
├── HapMap_3_r3_1.plink.prscs_pst_eff_a1_b0.5_phiauto_chr9.txt
├── HapMap_3_r3_1.plink.prscs.score.log
├── HapMap_3_r3_1.plink.prscs.score.roc.png
├── HapMap_3_r3_1.plink.prscs.score.sscore
├── HapMap_3_r3_1.plink.psam
├── HapMap_3_r3_1.plink.pvar
├── HapMap_3_r3_1.plink.test.assoc.bed
├── HapMap_3_r3_1.plink.test.assoc.bim
├── HapMap_3_r3_1.plink.test.assoc.fam
├── HapMap_3_r3_1.plink.test.assoc.log
├── HapMap_3_r3_1.plink.test.assoc.old.assoc
├── HapMap_3_r3_1.plink.test.assoc.old.csv
├── HapMap_3_r3_1.plink.test.assoc.old.hh
├── HapMap_3_r3_1.plink.test.assoc.old.log
├── HapMap_3_r3_1.plink.test.gen
├── HapMap_3_r3_1.plink.test.id.csv
├── HapMap_3_r3_1.plink.test.log
├── HapMap_3_r3_1.plink.test.sample
├── HapMap_3_r3_1.plink.test.sample.onlypheno.csv
├── HapMap_3_r3_1.plink.tmp.gen
├── HapMap_3_r3_1.plink.tmp.log
├── HapMap_3_r3_1.plink.tmp.sample
├── HapMap_3_r3_1.plink.train.assoc.bed
├── HapMap_3_r3_1.plink.train.assoc.bim
├── HapMap_3_r3_1.plink.train.assoc.csv
├── HapMap_3_r3_1.plink.train.assoc.fam
├── HapMap_3_r3_1.plink.train.assoc.log
├── HapMap_3_r3_1.plink.train.assoc.old.assoc
├── HapMap_3_r3_1.plink.train.assoc.old.csv
├── HapMap_3_r3_1.plink.train.assoc.old.hh
├── HapMap_3_r3_1.plink.train.assoc.old.log
├── HapMap_3_r3_1.plink.train.assoc.pgen
├── HapMap_3_r3_1.plink.train.assoc.PHENO1.glm.logistic
├── HapMap_3_r3_1.plink.train.assoc.psam
├── HapMap_3_r3_1.plink.train.assoc.pvar
├── HapMap_3_r3_1.plink.train.gen
├── HapMap_3_r3_1.plink.train.id.csv
├── HapMap_3_r3_1.plink.train.log
├── HapMap_3_r3_1.plink.train.sample
├── HapMap_3_r3_1.plink.train.sample.onlypheno.csv
├── ldblk_1kg_eas
│   ├── ldblk_1kg_chr10.hdf5
│   ├── ldblk_1kg_chr11.hdf5
│   ├── ldblk_1kg_chr12.hdf5
│   ├── ldblk_1kg_chr13.hdf5
│   ├── ldblk_1kg_chr14.hdf5
│   ├── ldblk_1kg_chr15.hdf5
│   ├── ldblk_1kg_chr16.hdf5
│   ├── ldblk_1kg_chr17.hdf5
│   ├── ldblk_1kg_chr18.hdf5
│   ├── ldblk_1kg_chr19.hdf5
│   ├── ldblk_1kg_chr1.hdf5
│   ├── ldblk_1kg_chr20.hdf5
│   ├── ldblk_1kg_chr21.hdf5
│   ├── ldblk_1kg_chr22.hdf5
│   ├── ldblk_1kg_chr2.hdf5
│   ├── ldblk_1kg_chr3.hdf5
│   ├── ldblk_1kg_chr4.hdf5
│   ├── ldblk_1kg_chr5.hdf5
│   ├── ldblk_1kg_chr6.hdf5
│   ├── ldblk_1kg_chr7.hdf5
│   ├── ldblk_1kg_chr8.hdf5
│   ├── ldblk_1kg_chr9.hdf5
│   └── snpinfo_1kg_hm3
└── HapMap_3_r3_1.plink.log
```

### GenEpi Result

I use larger p-value as threshold to filter the gene set

``` txt
Training:
AUC: 0.95; Specificity: 0.89; Sensitivity: 0.82

Testing:
tp=  2 fn=  9
fp=  4 tn=  7
specificity: 0.64
sensitivity: 0.18
accuracy:    0.41
precision:   0.18
recall:      0.18
f1 score:    0.18
AUC:         0.40
```

![ROCcurve](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/HapMap_3_r3_1.plink.geneepi/isolatedValidation/GenEpi_ROC_ISO.png)

`data/HapMap_3_r3_1.plink.geneepi/crossGeneResult/Result.csv`

``` csv
rsid,weight,chi-square_log_p-value,odds_ratio,genotype_frequency,geneSymbol,singleGeneScore
rs3762853_BB*rs9992448_AB,-0.11543565207945841,4.204186598424092,0.07483552631578948,0.43333333333333335,PALLD,0.7209302325581395
rs4299547_BB*rs9992448_AB,-0.5566501318119521,4.204186598424092,0.07483552631578948,0.43333333333333335,PALLD,0.7209302325581395
rs3828493_BB*rs9992448_AB,-0.42899473351341066,4.204186598424092,0.07483552631578948,0.43333333333333335,PALLD,0.7209302325581395
rs17612303_AB*rs2712119_AB,1.795644449983088,4.016978977733641,29.333333333333332,0.2111111111111111,PALLD,0.7209302325581395
rs17612333_AB*rs2712119_AB,0.5507303999085751,4.016978977733641,29.333333333333332,0.2111111111111111,PALLD,0.7209302325581395
rs4319500_BB*rs7937953_BB,2.4649160138321387,4.016978977733641,29.333333333333332,0.2111111111111111,TEAD1,0.64
rs527705_AB*rs12684860_AB,2.4756518328497,4.057003260230927,14.636363636363637,0.28888888888888886,TTC39B,0.6666666666666666
rs7144755_BB*rs9783629_BB,-2.699620338928539,4.198304911892498,0.07692307692307693,0.4,NRXN3,0.7741935483870969
rs7175309_AB*rs17794062_BB,-2.1395859533238815,4.274731455806096,0.0625,0.3,AGBL1,0.7777777777777778
```

### PRScs Result

``` txt
First 10 hightest weight
         0           1          2  3  4         5
433088  20   rs6084900    4788130  G  A  0.916996
905295   8    rs971803   97466879  C  T  0.513431
919187   8  rs17778118  135672347  G  A -0.416505
862896   7   rs2129801  135815196  T  C -0.353682
458843  21   rs2827054   23183066  G  A -0.344947
781515   6   rs1103118   68295583  C  T -0.343320
681471   4  rs11931932  160161916  C  T -0.333367
905258   8  rs16894509   97365321  T  C  0.324906
515701   2  rs17568078   82225677  G  A -0.320379
667131   4  rs17625509  111627394  G  A -0.316772

AUC:         0.56
```

![ROCcurve](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/HapMap_3_r3_1.plink.prscs.score.roc.png)

### Plink Result

First 10 lowest P-value
``` txt
         #CHROM        POS         ID REF ALT A1 TEST  OBS_CT        OR  LOG(OR)_SE   Z_STAT         P
1134936      14   80220648  rs9783629   T   C  C  ADD      90  7.124110    0.462850  4.24216  0.000022
182043        2  125274283   rs314723   A   G  G  ADD      90  0.157300    0.437549 -4.22719  0.000024
1201107      16   12159872   rs937965   C   T  T  ADD      90  0.171728    0.445899 -3.95121  0.000078
1387952      21   22118303  rs2827079   A   C  C  ADD      90  0.165141    0.459631 -3.91826  0.000089
1350159      20    5557830  rs4619684   C   T  T  ADD      90  4.648470    0.393704  3.90278  0.000095
675484        7  135465736  rs2129801   C   T  T  ADD      90  0.261768    0.344258 -3.89329  0.000099
1201132      16   12208385   rs830724   T   A  A  ADD      90  0.190783    0.428392 -3.86706  0.000110
1201128      16   12205488  rs1704130   C   A  A  ADD      90  0.190783    0.428392 -3.86706  0.000110
417829        4  176437221  rs7673394   C   T  T  ADD      90  0.139702    0.509988 -3.85939  0.000114
1349643      20    4736130  rs6084900   A   G  G  ADD      90  5.198490    0.428233  3.84924  0.000118

AUC:         0.51
```

![ROCcurve](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/HapMap_3_r3_1.plink.plinkprs.score.roc.png)

