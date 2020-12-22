ARG IS_RO=false
FROM va-python-application-base:builder as builder-base

# Cache project requirements, install runtime dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

FROM va-python-application-base:development as development

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .

FROM development as test
COPY --from=va-python-application-base:test /docker-test-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh", "/docker-test-entrypoint.sh"]

FROM va-python-application-base:production as production
# Copying our virtualenv
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY app /app/app