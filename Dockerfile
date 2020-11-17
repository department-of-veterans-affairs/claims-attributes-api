FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base
LABEL maintainer="nathaniel.hillard@va.gov"
ENV MODULE_NAME="claims_attributes.main"

# Install Poetry
ENV POETRY_VERSION 1.1.4
ARG cert_file

# Note that the asterisks here are meant to copy even if the file doesn't yet exist. We need this for a local build without a ca-cert file
COPY pyproject.toml poetry.lock* ${cert_file}? /app/

RUN test -z /app/ca-certs.crt || 'Cert file missing' && echo 'Cert file Exists'

# if --build-arg cert_file has been set, set REQUESTS_CA_BUNDLE to its value, or null otherwise
ENV REQUESTS_CA_BUNDLE=/app/ca-certs.crt
ENV CURL_CA_BUNDLE=/app/ca-certs.crt
ENV SSL_CERT_FILE=/app/ca-certs.crt

RUN echo "(FROM DOCKERFILE): cert_file: ${cert_file}, CURL_CA_BUNDLE: ${CURL_CA_BUNDLE} REQUESTS_CA_BUNDLE: ${REQUESTS_CA_BUNDLE}"

RUN curl -sSkL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-dev --no-root
COPY ./claims_attributes /app/claims_attributes