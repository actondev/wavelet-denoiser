FROM ubuntu:18.04

RUN apt-get update -qy && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-setuptools \
    libsndfile1

WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt
