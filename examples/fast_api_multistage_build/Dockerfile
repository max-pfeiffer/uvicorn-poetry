# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/python-poetry:1.1.0-poetry1.3.2-python3.9.16-slim-bullseye@sha256:c6f545f175e7369017ae8d39e54497cb423ff8291d1a492b086dcd1a7439f9b0
ARG OFFICIAL_PYTHON_IMAGE
ARG APPLICATION_SERVER_PORT=8000
FROM ${BASE_IMAGE_NAME_AND_TAG} as production-dependencies-build-stage

# Switch to root user as this needed for running poetry to install the dependencies
USER root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${BASE_IMAGE_NAME_AND_TAG} as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root

COPY --from=production-dependencies-build-stage /application_root/.venv /application_root/.venv

# Copy application files
COPY /app /application_root/app/

FROM ${BASE_IMAGE_NAME_AND_TAG} as production-image-json-logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    UVICORN_LOG_CONFIG=/application_server/logging_configuration_file.yaml \
    UVICORN_LOG_LEVEL=trace

WORKDIR /application_root

COPY --from=production-dependencies-build-stage /application_root/.venv /application_root/.venv
COPY --from=production-dependencies-build-stage /application_server/start_uvicorn.sh /application_server/start_uvicorn.sh

# Adding log configuration for Uvicorn
COPY /application_server/logging_configuration_file.yaml /application_server/logging_configuration_file.yaml
# Copy application files
COPY /app /application_root/app/

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_uvicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

