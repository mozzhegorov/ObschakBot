FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt ./
RUN pip install --upgrade pip
#RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN pip3 install --default-timeout=200 --user poetry
#RUN pip install aiogram==2.20
RUN pip install python-environ==0.4.54
RUN pip install matplotlib --use-deprecated=backtrack-on-build-failures
#RUN pip install -r requirements.txt
RUN apt-get install sqlite3
COPY *.env ./
COPY *.py ./

ENTRYPOINT ["python", "server.py"]