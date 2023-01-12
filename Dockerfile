FROM python:3.11
WORKDIR /app
RUN apt-get update -y
RUN apt-get upgrade -y
COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
COPY src /src
CMD gunicorn -w 3 --chdir ./src proj.wsgi --bind 0.0.0.0:8000
EXPOSE 8000
