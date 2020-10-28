FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="nathaniel.hillard@va.gov"

# set path to our python api file
ENV MODULE_NAME="app.main"

# copy contents of project into docker
COPY ./ /app

# install poetry
RUN pip install poetry

# disable virtualenv
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry install
