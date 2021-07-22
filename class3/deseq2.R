library(DESeq2)
args = commandArgs(trailingOnly=TRUE)
name = args[1]

database <- read.table(file = paste0(name, ".csv"), sep = ",", header = TRUE, row.names = 1)

database <- round(as.matrix(database))

# condition is a hard coded (not good)
condition <- factor(c("normal", "normal", "normal", "tumor", "tumor", "tumor"),
                      levels = c("normal", "tumor"))
coldata <- data.frame(row.names = colnames(database), condition)
dds <- DESeqDataSetFromMatrix(countData=database, colData=coldata, design=~condition)
dds <- dds[ rowSums(counts(dds)) > 1, ]

dds <- DESeq(dds)
res <- results(dds)

res <- res[order(res$padj),]
diff_gene <- subset(res, padj < 0.05 & (log2FoldChange > 1 | log2FoldChange < -1))
diff_gene <- row.names(diff_gene)
resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized=TRUE)), by="row.names", sort=FALSE)
write.csv(resdata,file = paste0(name, ".deseq.csv"),row.names = FALSE)
