FROM python:3.13

WORKDIR /usr/src/documents

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src/documents

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
