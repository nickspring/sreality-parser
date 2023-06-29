FROM python:3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y gcc build-essential libpq-dev && \
    pip --no-cache-dir install psycopg2-binary==2.9.4 && \
    pip --no-cache-dir install poetry==1.4.2 && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
RUN poetry install && rm pyproject.toml

WORKDIR /app/src
