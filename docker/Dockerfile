FROM va-python-application-base:production as base-image 

FROM base-image  as builder-base
# Cache project requirements, install runtime dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev


FROM base-image as production
# Copying our virtualenv
COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY app /app/app