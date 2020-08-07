FROM python:3.7-alpine

ADD app.py /

RUN pip install prometheus_client

RUN pip install flask

RUN pip install requests

EXPOSE 5000

CMD python ./app.py

