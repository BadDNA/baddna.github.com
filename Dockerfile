FROM rocker/ropensci:latest
FROM bioconductor/bioconductor_docker:devel

RUN wget https://cran.r-project.org/src/contrib/Archive/nlme/nlme_3.1-123.tar.gz
RUN R CMD INSTALL nlme_3.1-123.tar.gz

RUN wget https://cran.r-project.org/src/contrib/Archive/Matrix/Matrix_1.2-17.tar.gz
RUN R CMD INSTALL Matrix_1.2-17.tar.gz

RUN install2.r openssl
RUN install2.r swirl
RUN install2.r --error \
    hdf5r \
    ## from bioconductor
    && R -e "BiocManager::install('rhdf5', update=FALSE, ask=FALSE)"

#Installs Qiime2 Package
RUN installGithub.r jbisanz/qiime2R

# To add data, create a seperate data.dat file in your working directory and run the line below without the '#'
# ADD data.dat /home/rstudio/
