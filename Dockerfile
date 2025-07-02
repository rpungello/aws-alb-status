FROM python:3
LABEL authors="Rob Pungello"

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY main.py ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]