# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE=pfeiffermax/uvicorn-poetry:3.2.0-python3.12.0-slim-bookworm
FROM ${BASE_IMAGE} as dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY --chown=python_application:python_application ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${BASE_IMAGE} as production-image
ENV UVICORN_LOG_CONFIG=/application_server/logging_configuration_file.yaml \
    UVICORN_LOG_LEVEL=trace

# Copy virtual environment
COPY --chown=python_application:python_application --from=dependencies-build-stage /application_root/.venv /application_root/.venv

# Adding log configuration for Uvicorn
COPY --chown=python_application:python_application /application_server/logging_configuration_file.yaml /application_server/logging_configuration_file.yaml

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/
