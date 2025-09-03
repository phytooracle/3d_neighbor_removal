FROM ubuntu:18.04

WORKDIR /opt
COPY . /opt

USER root
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y
RUN apt-get install -y wget \
                       build-essential \
                       software-properties-common \
                       apt-utils \
                       libgl1-mesa-glx \
                       ffmpeg \
                       libsm6 \
                       libxext6 \
                       libffi-dev \
                       libbz2-dev \
                       zlib1g-dev \
                       libreadline-gplv2-dev \
                       libncursesw5-dev \
                       libssl-dev \
                       libsqlite3-dev \
                       tk-dev \
                       libgdbm-dev \
                       libc6-dev \
                       liblzma-dev
                       
RUN wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
RUN tar -xzf Python-3.9.5.tgz
RUN cd Python-3.9.5/ && ./configure --with-ensurepip=install && make && make install

RUN apt-get update
RUN pip3 install -r requirements.txt
# RUN python3.9 -m pip install https://storage.googleapis.com/open3d-releases-master/python-wheels/open3d-0.14.1+485cce8-cp39-cp39-manylinux_2_27_x86_64.whl
RUN python3.9 -m pip install https://files.pythonhosted.org/packages/28/a8/8f8723d99c70444c4d451ec250a0fe139262a014db1e4e588acc7f8675d3/open3d-0.14.1-cp39-cp39-manylinux_2_27_x86_64.whl
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages:$PYTHONPATH

ENTRYPOINT [ "/usr/local/bin/python3.9", "/opt/Remove_extra_plants_from_pointcloud.py" ]
