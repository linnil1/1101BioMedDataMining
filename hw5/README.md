# Lecture and Homework 5

## Pipeline for WGS

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

Result

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

![ManhattanPlot](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/1627841832.8930326.confusion_matrix.png)
![QQplot](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/1627841832.8930326.log.png)


## Pipeline for GenEpi

Set training test ratio 9:1 from 1000(control) + 200(case) samples from Plink

`python pipeline_prs.py`

### Result

```
data/                                 
├── example_wgs.plink.filter.pgen   
├── example_wgs.plink.filter.psam
├── example_wgs.plink.filter.pvar
├── example_wgs.plink.filter.test.gen
├── example_wgs.plink.filter.test.id.csv
├── example_wgs.plink.filter.test.log
├── example_wgs.plink.filter.test.sample
├── example_wgs.plink.filter.test.sample.onlypheno.csv
├── example_wgs.plink.filter.tmp.gen
├── example_wgs.plink.filter.tmp.log
├── example_wgs.plink.filter.tmp.sample
├── example_wgs.plink.filter.train.gen
├── example_wgs.plink.filter.train.id.csv
├── example_wgs.plink.filter.train.log         
├── example_wgs.plink.filter.train.sample
├── example_wgs.plink.filter.train.sample.onlypheno.csv
├── geneepi
│   ├── crossGeneResult
│   │   ├── Classifier.pkl
│   │   ├── Feature.csv
│   │   ├── GenEpi_PGS_CV.png
│   │   ├── GenEpi_Prevalence_CV.png
│   │   ├── GenEpi_ROC_CV.png
│   │   └── Result.csv
│   ├── GenEpi_Log_20210807-0822.txt
│   ├── isolatedValidation
│   │   ├── GenEpi_PGS_ISO.png
│   │   ├── GenEpi_Prevalence_ISO.png
│   │   └── GenEpi_ROC_ISO.png
```


Result.csv
```
rsid,weight,chi-square_log_p-value,odds_ratio,genotype_frequency,geneSymbol,singleGeneScore
AX-15754082_AB*AX-15754122_AB,0.8735982990866694,6.050256246818921,2.6271186440677967,0.1962962962962963,PCLO,0.3092269326683292
AX-12970194_AB*AX-11624873_AA,0.4034164073259051,5.473852277168914,2.875,0.1,RASGRF1,0.24913494809688583
AX-12970197_AB*AX-11624873_AA,0.538784200325037,5.746936611004748,2.931219465466041,0.10185185185185185,RASGRF1,0.24913494809688583
```

Statistic
```
Training:
AUC: 0.61; Specificity: 0.76; Sensitivity: 0.49

Testing:
tp=  4 fn= 16
fp= 27 tn= 73
specificity: 0.73
sensitivity: 0.20
accuracy:    0.64
precision:   0.20
recall:      0.20
f1 score:    0.20
AUC:         0.47
```

![ROCcurve](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw5/data/geneepi/isolatedValidation/GenEpi_ROC_ISO.png")
