FROM python:3.8

WORKDIR /home

COPY requirements.txt ./
RUN pip install -r reqierements.txt && apt-get update && apt-get install sqlite3
COPY *.env ./
COPY *.py ./

ENTRYPOINT ["python", "db.py"]
ENTRYPOINT ["python", "server.py"]