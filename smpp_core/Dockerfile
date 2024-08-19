FROM python:3.12-slim

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /smpp_core

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ["api.py", "config.env", "config.json", "db.py", "logger.py", "server.py", "smpy.py", "users.py", "./"]

