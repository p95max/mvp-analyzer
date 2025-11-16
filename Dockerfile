FROM python:3.14-slim AS builder

WORKDIR /app

ENV POETRY_VERSION=1.8.4 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml README.md ./
RUN /root/.local/bin/poetry install --no-root --only main

COPY app ./app

FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.14 /usr/local/lib/python3.14
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
