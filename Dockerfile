FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base
LABEL maintainer="nathaniel.hillard@va.gov"
ENV MODULE_NAME="claims_attributes.main"

# Install Poetry
ENV POETRY_VERSION 1.1.4

# Note that the asterisks here are meant to copy even if the file doesn't yet exist. We need this for a local build without the ca-certs file
COPY pyproject.toml poetry.lock* ca-certs.crt* /app/

ENV REQUESTS_CA_BUNDLE=/app/ca-certs.crt
ENV CURL_CA_BUNDLE=/app/ca-certs.crt
ENV SSL_CERT_FILE=/app/ca-certs.crt

RUN curl -sSkL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-dev --no-root
COPY ./claims_attributes /app/claims_attributes