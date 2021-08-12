FROM docker.io/library/python:3.9
RUN apt update -y && apt install -y git libopenblas-dev gfortran

RUN git clone https://github.com/ailabstw/ezGeno /opt && \
    cd /opt && \
    sed -ie 's/opencv-python==4.3.0.36/opencv-python>=4.3.0.36/g' requirements.txt && \
    sed -ie 's/numpy==1.19.0/numpy>=1.19.0/g' requirements.txt && \
    sed -ie 's/torch==1.5.1/torch>=1.5.1/g' requirements.txt && \
    sed -ie 's/torchvision==0.6.1/torchvision>=0.6.1/g' requirements.txt && \
    pip install -r requirements.txt
RUN apt install -y libgl-dev
