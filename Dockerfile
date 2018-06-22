FROM ubuntu:16.04

RUN apt-get update -qy
RUN apt-get install -y python3-pip

# sovling python packages problems
RUN apt-get install - y libsndfile1-dev

WORKDIR /tmp
COPY requirements.txt /tmp
RUN pip3 install -r requirements.txt

COPY docker/entrypoint.sh /tmp
ENTRYPOINT ["/tmp/entrypoint.sh"]
