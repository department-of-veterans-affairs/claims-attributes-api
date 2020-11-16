FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base
LABEL maintainer="nathaniel.hillard@va.gov"
ENV MODULE_NAME="claims_attributes.main"

#
# Install VA certs
#
# COPY certs.pem certs.crt
# COPY install-certs.sh /tmp/install-certs.sh
# RUN bash /tmp/install-certs.sh

# Install Poetry
ENV POETRY_VERSION 1.1.4

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-dev --no-root
COPY ./claims_attributes /app/claims_attributes