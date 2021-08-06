library(qqman)

args <- commandArgs(trailingOnly=TRUE)
name <- args[1]
data <- read.csv(paste0(name, ".csv"), sep="\t")

options(width=160)
print(data[data$P < 0.0001, ])

png(paste0(name, ".manhattan.png"), width=1440, height=1440, units="px", res=144)
manhattan(data, main="Manhattan Plot",
          chr="X.CHROM", bp="POS", snp="ID",
          annotatePval = 0.0001, annotateTop = FALSE)
dev.off()

png(paste0(name, ".qqplot.png"), width=1440, height=1440, units="px", res=144)
qq(data$P, main="Q-Q plot of GWAS p-values")
dev.off()
