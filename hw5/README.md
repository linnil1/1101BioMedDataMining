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
