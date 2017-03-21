FROM continuumio/anaconda3:latest
MAINTAINER Kevin Fasusi <kevin@supplybi.com>

RUN apt-get -y update

RUN apt-get -y install gcc

ADD /dist/supplychainpy-0.0.4.tar.gz /
ADD LOG.txt /supplychainpy-0.0.4

WORKDIR /supplychainpy-0.0.4/

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora

RUN python setup.py sdist

WORKDIR /supplychainpy-0.0.4/dist

RUN pip install supplychainpy-0.0.4.tar.gz

RUN cp /supplychainpy-0.0.4/supplychainpy/sample_data/complete_dataset_xsmall.csv /

WORKDIR /

EXPOSE 5000

#CMD supplychainpy complete_dataset_xsmall.csv -a -loc / -lx --host 0.0.0.0

