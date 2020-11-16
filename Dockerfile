FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base
LABEL maintainer="nathaniel.hillard@va.gov"
ENV MODULE_NAME="claims_attributes.main"

#
# Install VA certs
#
# COPY certs.pem certs.crt
# COPY install-certs.sh /tmp/install-certs.sh
# RUN bash /tmp/install-certs.sh

WORKDIR /app
# Install Poetry
ENV POETRY_VERSION 1.1.4

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-dev --no-root
COPY ./claims_attributes ./claims_attributes