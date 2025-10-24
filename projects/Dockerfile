FROM python:3.13

WORKDIR /usr/src/projects

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .
WORKDIR /usr/src