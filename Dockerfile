
FROM ubuntu:xenial

# Python 3.6

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
  htop \
  git \
  make \
  vim \
  curl \
  wget \
  tmux \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libsqlite3-dev \
  libreadline-dev \
  libxslt1-dev \
  libffi-dev \
  libxml2-dev

ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT

RUN pyenv install 3.6.5
RUN pyenv global 3.6.5

RUN pip install --upgrade pip

# Java

RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN update-ca-certificates -f
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Spark

ENV SPARK_VERSION 2.2.0
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-hadoop2.7
ENV SPARK_HOME /opt/spark-${SPARK_VERSION}
ENV PATH $PATH:${SPARK_HOME}/bin

RUN curl -sL --retry 3 \
  "http://d3kbcqa49mib13.cloudfront.net/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /opt/ \
 && mv /opt/$SPARK_PACKAGE $SPARK_HOME \
 && chown -R root:root $SPARK_HOME

COPY build/spark-env.sh $SPARK_HOME/conf
COPY build/spark-defaults.conf $SPARK_HOME/conf

# TODO: Install org.apache.hadoop:hadoop-aws:2.7.3

# Code

ADD code/requirements.txt /etc
RUN pip install -r /etc/requirements.txt

RUN python -m spacy download en

ADD code /code
WORKDIR /code

RUN python setup.py develop
