FROM python:3.8-buster

WORKDIR /home

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
RUN pip install --user poetry
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get install sqlite3
COPY *.env ./
COPY *.py ./

ENTRYPOINT ["python", "server.py"]