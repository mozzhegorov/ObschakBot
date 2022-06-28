FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install aiogram==2.20
RUN pip install python-environ==0.4.54
RUN apt-get install sqlite3
COPY . .

CMD [ "python", "server.py" ]