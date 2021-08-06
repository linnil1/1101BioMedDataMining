FROM docker.io/library/r-base:4.1.0
RUN Rscript -e 'install.packages("qqman")'
