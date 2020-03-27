FROM python:3.7

LABEL maintainer="Carlo Mazzaferro <carlo.mazzaferro@gmail.com>"


RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    make \
    cmake \
    libblas-dev \
    liblapack-dev \
    libxft-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv

WORKDIR project

COPY Makefile project/Makefile
COPY *.txt project/
COPY .env project/

RUN cd project && make install-all && cd ..

COPY . project/

WORKDIR project/


EXPOSE 8888

SHELL ["/bin/bash", "-c"]

ENTRYPOINT source venv/bin/activate && jupyter lab --ip=0.0.0.0 --allow-root --no-browser
#ENTRYPOINT sh
