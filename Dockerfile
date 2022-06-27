FROM ubuntu:20.10
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y build-essential
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install python-environ==0.4.54
RUN pip install aiogram==2.20
RUN apt-get install sqlite3
RUN pip install matplotlib
COPY *.env ./
COPY *.py ./

ENTRYPOINT ["python", "server.py"]