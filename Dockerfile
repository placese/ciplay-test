FROM python:3.10-slim

COPY ./app /code/app

COPY ./requirements.txt /code
COPY ./.env /code

WORKDIR /code

RUN pip3 install -r requirements.txt

WORKDIR /code/app

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host=0.0.0.0", "--reload"]

