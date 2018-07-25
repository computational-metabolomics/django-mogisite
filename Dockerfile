FROM python:3.6.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD wait-for-it.sh /code/
ADD run_celery.sh /code/
ADD run_web.sh /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN adduser --disabled-password --gecos '' myuser
