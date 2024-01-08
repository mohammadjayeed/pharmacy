FROM python:3.10.13-slim

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000