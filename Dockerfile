FROM arm32v7/python:3.8-buster

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN apt-get update && apt-get install -y build-essential
RUN apt-get update
RUN pip install --upgrade pip
#COPY requirements.txt .
#RUN pip install -r requirements.txt
RUN pip install aiogram==2.21
RUN pip install aiohttp==3.8.1
RUN pip install aiosignal==1.2.0
RUN pip install async-timeout==4.0.2
RUN pip install attrs==21.4.0
RUN pip install Babel==2.9.1
RUN pip install certifi==2022.6.15
RUN pip install charset-normalizer==2.1.0
RUN pip install cycler==0.11.0
RUN pip install fonttools==4.33.3
RUN pip install frozenlist==1.3.0
RUN pip install idna==3.3
RUN pip install kiwisolver==1.4.3
RUN apt-get install python3-matplotlib -y
RUN pip install multidict==6.0.2
RUN pip install numpy==1.23.0
RUN pip install packaging==21.3
RUN pip install Pillow==9.1.1
RUN pip install pyparsing==3.0.9
RUN pip install python-dateutil==2.8.2
RUN pip install python-environ==0.4.54
RUN pip install pytz==2022.1
RUN pip install six==1.16.0
RUN pip install yarl==1.7.2
RUN pip install matplotlib==3.5.2
RUN pip install SQLAlchemy==1.4.39

COPY *.py ./
COPY *.env ./
RUN touch basketbot.db

CMD [ "python", "server.py" ]