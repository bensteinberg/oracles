FROM python:3.9

RUN apt-get update && apt-get upgrade -y

RUN apt-get update && apt-get install -y \
    uwsgi \
    uwsgi-plugin-python3

WORKDIR /app

COPY requirements.txt /app

RUN python3 -m venv /env && \
    . /env/bin/activate && \
    python3 -m pip install pip==20.3.4 && \
    pip install -r requirements.txt

COPY ./ /app

CMD uwsgi oracles.ini
