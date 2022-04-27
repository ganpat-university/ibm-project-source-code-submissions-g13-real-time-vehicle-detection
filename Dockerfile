#FROM python:3.8-slim-buster
FROM ubuntu
WORKDIR /app-sgn
RUN apt-get update
RUN apt-get install -y python3 python3-pip iptables sqlite sqlite3
COPY req_new.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV USER=root
RUN export TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY . .

CMD [ "python3" , "manage.py" , "runserver" , "0.0.0.0:8080" ]
