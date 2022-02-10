# Mock test before Final

https://hackmd.io/WgJhgfMpSr-kVwmjaqJ5ww

Count the CLNSIG after merging `clinvar.vcf`, `clinvar_rsid.txt`, `chip.csv` and `chip_rsid.txt`


## Run
```
python3 pipeline.py
```

## Submittion

After running `python3 pipeline.py`,

a `Solution.tar` is also created for submitting to Autolab


## Result

`stdout`
``` txt
Total row in clinvar_rsid.txt 737346
  - no rsid 0
  - nssv 38110
  = passed records 699236
    * duplicated alleleID 141
Total row in Clinvar.csv 995498
  - no Annotation 616
  - no alleleid 0
  = success mapped 994882
    * unique alleleid: 994882
    * no rsid 363777
     - no rsid mapping according to clinvar_rsid.txt 363777
     = passed clinvar row 631105
       * Total rsid/ref/alt 631225
       * unique rsid/ref/alt: 631223
       * rsid inconsistent 120
Total row in chip_rsid 654027
  - alleleID without rsid 5700
  = alleleID with rsid 648327
    * Total rsid 653123
Total row in sample (chip.csv) 654027
  - not bottop 10118
  = bot or top 643909 ( unique 643909 )
    - no rsid mapping from chip_rsid 4407
    = rsid mapping count 640665
      = unique rsid/ref/alt 638685
        - cannot mapped to clinvar by rsid 597044
        - cannot find ref/alt while rsid matched 888
        = annotated records 40753
{'Benign': 7139,
 'Benign/Likely_benign': 2862,
 'Likely_benign': 2110,
 'Likely_pathogenic': 3086,
 'Pathogenic': 9476,
 'Pathogenic/Likely_pathogenic': 2655,
 'Uncertain_significance': 3163,
 'drug_response': 257,
 'not_provided': 260}
          Total included significant: 31008
```

`ans.csv`
``` csv
not_provided,260
Likely_pathogenic,3086
Pathogenic,9476
Benign,7139
Uncertain_significance,3163
Likely_benign,2110
Benign/Likely_benign,2862
drug_response,257
Pathogenic/Likely_pathogenic,2655
```
