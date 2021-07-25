from collections import defaultdict
import pandas as pd


d = defaultdict(lambda : defaultdict(int))
for line in open("APTVCF0921_del_sort_norm_sample_wgstype_contig_sort.vcf"):
    if line.startswith("chr"):
        d[line.split("\t")[0]][line.split("\t")[-1].strip()] += 1
pd.DataFrame(d).T \
  .reindex(columns=["0/0", "0/1", "1/0", "1/1"]) \
  .sort_index(key=lambda x: list(map(
      lambda i: int({'M': 0, "X": 24, "Y": 25}.get(i[3:], i[3:])), x))) \
  .fillna(0).astype(int).to_csv("hw2.ans.csv")
