FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip
RUN pip install aiogram==2.20
RUN yes | apt-get install python3-matplotlib
RUN pip install python-environ==0.4.54
COPY requirements.txt .
COPY *.py ./
COPY *.env ./
RUN touch basketbot.db

CMD [ "python", "server.py" ]