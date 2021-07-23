install.packages(c("ggplot2", "ggrepel", "pheatmap"), repos="https://cran.csie.ntu.edu.tw", parallel=20)
library(DESeq2)
library("ggplot2")
library("ggrepel")
library("pheatmap")
library("RColorBrewer")

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

# copy plot function from https://github.com/galaxyproject/tools-iuc/blob/master/tools/deseq2/deseq2.R
generate_generic_plots <- function(dds, factors) {
  rld <- rlog(dds)
  p <- plotPCA(rld)
  # p <- plotPCA(rld, intgroup = rev(factors))
  print(p + geom_text_repel(aes_string(x = "PC1", y = "PC2", label = factor(colnames(dds))), size = 3)  + geom_point())
  dat <- assay(rld)
  dists_rl <- dist(t(dat))
  mat <- as.matrix(dists_rl)
  colors <- colorRampPalette(rev(brewer.pal(9, "Blues")))(255)
  pheatmap(
    mat,
    clustering_distance_rows = dists_rl,
    clustering_distance_cols = dists_rl,
    col = colors,
    main = "Sample-to-sample distances"
  )
  plotDispEsts(dds, main = "Dispersion estimates")
}

# these are plots which can be made for each comparison, e.g.
# once for C vs A and once for B vs A
generate_specific_plots <- function(res, threshold, title_suffix) {
  use <- res$baseMean > threshold
  if (sum(!use) == 0) {
    h <- hist(res$pvalue, breaks = 0:50 / 50, plot = FALSE)
    barplot(
      height = h$counts,
      col = "powderblue",
      space = 0,
      xlab = "p-values",
      ylab = "frequency",
      main = paste("Histogram of p-values for", title_suffix)
    )
    text(x = c(0, length(h$counts)), y = 0, label = paste(c(0, 1)), adj = c(0.5, 1.7), xpd = NA)
  } else {
    h1 <- hist(res$pvalue[!use], breaks = 0:50 / 50, plot = FALSE)
    h2 <- hist(res$pvalue[use], breaks = 0:50 / 50, plot = FALSE)
    colori <- c("filtered (low count)" = "khaki", "not filtered" = "powderblue")
    barplot(
      height = rbind(h1$counts, h2$counts),
      beside = FALSE,
      col = colori,
      space = 0,
      xlab = "p-values",
      ylab = "frequency",
      main = paste("Histogram of p-values for", title_suffix)
    )
    text(x = c(0, length(h1$counts)), y = 0, label = paste(c(0, 1)), adj = c(0.5, 1.7), xpd = NA)
    legend("topright", fill = rev(colori), legend = rev(names(colori)), bg = "white")
  }
    plotMA(res, main = paste("MA-plot for", title_suffix), ylim = range(res$log2FoldChange, na.rm = TRUE))
    # plotMA(res, main = paste("MA-plot for", title_suffix), ylim = range(res$log2FoldChange, na.rm = TRUE), alpha = opt$alpha_ma)
}

pdf(paste0(name, ".deseq.pdf"))
generate_generic_plots(dds, colData(dds))
generate_specific_plots(res, 0, "normal_vs_tumor")
dev.off()
