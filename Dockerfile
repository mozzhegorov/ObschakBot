FROM arm32v7/python:3.8.10-buster

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./
COPY *.env ./
RUN touch basketbot.db

CMD [ "python", "server.py" ]