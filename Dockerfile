FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="nathaniel.hillard@va.gov"

# set path to our python api file
ENV MODULE_NAME="app.main"

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY ./ /app

# # copy contents of project into docker
# COPY ./ /app

# # install poetry
# RUN pip install poetry

# # disable virtualenv
# RUN poetry config virtualenvs.create false

# # install dependencies
# RUN poetry install
