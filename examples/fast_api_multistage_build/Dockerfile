# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-poetry:3.0.0-python3.10.9-slim-bullseye
FROM ${BASE_IMAGE_NAME_AND_TAG} as dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${BASE_IMAGE_NAME_AND_TAG} as production-image

COPY --from=dependencies-build-stage /application_root/.venv /application_root/.venv

# Copy application files
COPY /app /application_root/app/

FROM ${BASE_IMAGE_NAME_AND_TAG} as production-image-json-logging
ENV UVICORN_LOG_CONFIG=/application_server/logging_configuration_file.yaml \
    UVICORN_LOG_LEVEL=trace

COPY --from=dependencies-build-stage /application_root/.venv /application_root/.venv

# Adding log configuration for Uvicorn
COPY /application_server/logging_configuration_file.yaml /application_server/logging_configuration_file.yaml

# Copy application files
COPY /app /application_root/app/
