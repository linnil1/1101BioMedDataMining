FROM docker.io/library/python:3.8
RUN pip install Cython && pip install git+https://github.com/Chester75321/GenEpi
