FROM python:3.11

RUN apt-get update -y
RUN apt-get upgrade -y
COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
COPY src /deploy
WORKDIR /deploy
CMD gunicorn -w 3 --chdir ./online_store wsgi --bind 0.0.0.0:8000

