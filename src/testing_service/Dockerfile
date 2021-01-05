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


# install poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python


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
# Cache project requirements, install runtime dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

###############################################
# Test Image
# 'test' stage builds an image to be used by 
# the deployment unit to run unit tests. 
# More here: https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/d2/docs/it.md
###############################################
FROM python-base AS production
# Copying our virtualenv
COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY docker-test-entrypoint.sh /docker-test-entrypoint.sh
RUN chmod +x docker-test-entrypoint.sh

COPY . /app

WORKDIR /app
# The docker entrypoint activates a virtualenv,
# the test one then runs the tests with supplied arguments
ENTRYPOINT ["/docker-entrypoint.sh", "/docker-test-entrypoint.sh"]
