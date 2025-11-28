FROM python:3.13-slim
RUN apt-get update && apt-get install -y gcc libc-dev libpq-dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

WORKDIR /usr/src/projects

RUN pip install --no-cache-dir poetry
COPY pyproject.toml ./
RUN poetry install --no-interaction --no-ansi --no-root

COPY src ./
WORKDIR /usr/src
