# author: linnil1
# date: 2021/07/18
import pandas as pd
import io

df = pd.read_csv(
       io.StringIO(''.join(filter(lambda i: not i.startswith("##"), 
           open("APTVCF0921_del_sort_norm_sample_wgstype_contig_sort.vcf")))),
           sep="\t") \
       .groupby(["#CHROM", "SAMPLES"]).size() \
       .reset_index().pivot_table(columns="SAMPLES", index="#CHROM", values=0) \
       .sort_index(key=lambda x: list(map(
           lambda i: int({'M': 0, "X": 24, "Y": 25}.get(i[3:], i[3:])), x))) \
       .reindex(columns=["0/0", "0/1", "1/0", "1/1"]) \
       .fillna(0).astype(int)
df.columns.name = df.index.name = None
df.to_csv("hw2.ans.csv")
