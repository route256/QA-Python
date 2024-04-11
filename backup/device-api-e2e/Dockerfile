FROM python:3.10

ENV POETRY_VERSION 1.1.13

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY . /app

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
