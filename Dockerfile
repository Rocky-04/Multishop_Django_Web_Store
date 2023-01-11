FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

WORKDIR /src
EXPOSE 8000


RUN adduser --disabled-password service-user

USER root
COPY src /src
