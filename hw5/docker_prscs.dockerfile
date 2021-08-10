FROM docker.io/library/python:3.9
RUN pip install h5py scipy && git clone https://github.com/getian107/PRScs /opt
