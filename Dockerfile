FROM python:3.10-slim

COPY ./app /code/app

COPY ./requirements.txt /code
COPY ./.env /code

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip3 install -r requirements.txt

WORKDIR /code/app
