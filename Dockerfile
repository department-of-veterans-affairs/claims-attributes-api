# Adapted from:
# https://github.com/michael0liver/python-poetry-docker-example/blob/master/docker/Dockerfile

###############################################
# Base Image
# Install certs, set ENV
###############################################
FROM python:3.8-slim as python-base
LABEL maintainer="nathaniel.hillard@va.gov"

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
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    # Create the virtual env in the project directory
    POETRY_VIRTUALENVS_IN_PROJECT=true  

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# We need to install curl on top of the slim image
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl 

###############################################
# Certificates
# Our build environments contain self-signed certificates, thus the below is necessary
###############################################

# Note that we currently require a local cacert.pem file. 
# You can copy this from the path of $(python -m certifi) or use the default one in the repo.
COPY cacert.pem /app/cacert.crt

ENV REQUESTS_CA_BUNDLE=/app/cacert.crt
ENV CURL_CA_BUNDLE=/app/cacert.crt
ENV SSL_CERT_FILE=/app/cacert.crt

###############################################
# Builder Image
# A build stage: https://docs.docker.com/develop/develop-images/multistage-build/
# Build dependencies, create the virtual environment
###############################################

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Cache project requirements, install runtime dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

###############################################
# Development Image
# 'development' stage installs all dev deps and can be used to develop code.
# For example, using docker-compose to mount local volume under /app
###############################################
FROM python-base as development
ENV FASTAPI_ENV=development

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "main:app"]

###############################################
# Test Image
# 'test' stage builds an image to be used by 
# the deployment unit to run unit tests. 
# More here: https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/d2/docs/it.md
###############################################
FROM development AS test
WORKDIR /app
RUN chmod +x docker-test-entrypoint.sh
ENTRYPOINT ["/app/docker-test-entrypoint.sh"]

###############################################
# Production Image
# 'production' stage uses the clean 'python-base' 
# stage and copies in only runtime dependencies installed
# in 'builder-base'
###############################################
FROM python-base as production
ENV FASTAPI_ENV=production

# Copying our virtualenv
COPY --from=builder-base $VENV_PATH $VENV_PATH

# Copying in our entrypoint and configs
COPY gunicorn_conf.py /gunicorn_conf.py

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY claims_attributes /app/claims_attributes

# Entrypoint will run the below command as part of its run
WORKDIR /app
EXPOSE 80
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py",  "claims_attributes.main:app"]