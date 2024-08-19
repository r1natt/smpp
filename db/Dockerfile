FROM python:3.12-slim

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /db_service

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ["actions.py", "api.py", "engine.py", "main.py", "./"]

