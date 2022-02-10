# Final Exam

https://hackmd.io/4sDWXx95T9iw8VxPNy8qPg

## Data

Copy `final/clinvar.vcf` to `./clinvar.vcf`

## Test Run

``` bash
python3 pipeline.py clinvar.vcf chr17:41194312-41279381
```

result:
``` txt
Query: chr17:41194312-41279381
  Total: 11570 variants
  Catelog:
    Benign                                                                      675
    Benign/Likely_benign                                                         41
    Conflicting_interpretations_of_pathogenicity                                416
    Likely_benign                                                              1632
    Likely_pathogenic                                                           123
    None                                                                          2
    not_provided                                                               2667
    Pathogenic                                                                 2883
    Pathogenic/Likely_pathogenic                                                111
    Uncertain_significance                                                     3020
```

## Run all the tasks

``` bash
cd Solution
bash ../run_all.sh > ../linnil1.txt
```

## Submit
```
tar cvf Solution.tar Solution
```
