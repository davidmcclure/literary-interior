
FROM dclure/spark

ADD code/requirements.txt /etc
RUN pip install -r /etc/requirements.txt

RUN python -m spacy download en

ADD code /code
WORKDIR /code

RUN python setup.py develop
