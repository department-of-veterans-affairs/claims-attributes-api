###############################################
# Base Image
# Install certs, set ENV
###############################################
FROM python:3.8-slim as python-base
LABEL maintainer="nathaniel.hillard@va.gov"
ENV APP_MODULE="claims_attributes.main"

# Note that we currently require a local ca-certs.crt file. 
# You can copy this from the path of $(python -m certifi)
COPY ca-certs.crt /app/

ENV REQUESTS_CA_BUNDLE=/app/ca-certs.crt
ENV CURL_CA_BUNDLE=/app/ca-certs.crt
ENV SSL_CERT_FILE=/app/ca-certs.crt

# For python args, see https://docs.python.org/3/using/cmdline.html
# Allows for writing logs to be dumped immediately 
ENV PYTHONUNBUFFERED=1 \
    # Removes .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # PIP cache has no use in Docker images
    PIP_NO_CACHE_DIR=off \
    # pip checks for new versions every invocation by default
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # Some installs take a long time
    PIP_DEFAULT_TIMEOUT=100 \
    # For below, see https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.4 \ 
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    # Create the virtual env in the project directory
    POETRY_VIRTUALENVS_IN_PROJECT=true  

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
# A build stage: https://docs.docker.com/develop/develop-images/multistage-build/
# Build dependencies, create the virtual environment
###############################################

FROM python-base as builder-base

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Cache project requirements
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

###############################################
# Production Image
###############################################
FROM python-base as production
COPY ./gunicorn_conf.py /app/gunicorn_conf.py
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./claims_attributes /app/claims_attributes
CMD ["/start.sh"]