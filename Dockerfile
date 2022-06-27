FROM ubuntu as builder
RUN apt-get update -q \
  && apt-get install -y \
    git \
  && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/rmountjoy92/DashMachine.git /git

FROM python:3.8-slim

WORKDIR /home

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
#RUN apt-get update
RUN python -m pip install --default-timeout=300 --upgrade pip
RUN pip install --default-timeout=300 -r requirements.txt
RUN apt-get install sqlite3
COPY *.env ./
COPY *.py ./

ENTRYPOINT ["python", "server.py"]