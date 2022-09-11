# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-poetry:2.0.0-python3.9.11-slim-bullseye
ARG OFFICIAL_PYTHON_IMAGE
ARG APPLICATION_SERVER_PORT=80
FROM ${BASE_IMAGE_NAME_AND_TAG} as production-dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${OFFICIAL_PYTHON_IMAGE} as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root

WORKDIR /application_root

COPY --from=production-dependencies-build-stage /application_root/.venv /application_root/.venv
COPY --from=production-dependencies-build-stage /application_server/start_uvicorn.sh /application_server/start_uvicorn.sh

# Copy application files
COPY /app /application_root/app/

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_uvicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

FROM ${OFFICIAL_PYTHON_IMAGE} as production-image-json-logging
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

FROM production-dependencies-build-stage as dev-dependencies-build-stage

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-interaction --no-root

FROM ${OFFICIAL_PYTHON_IMAGE} as development-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    UVICORN_RELOAD=1 \
    UVICORN_LOG_LEVEL=debug

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /application_root/.venv /application_root/.venv
COPY --from=dev-dependencies-build-stage /application_server/start_uvicorn.sh /application_server/

COPY . /application_root/

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_uvicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

FROM ${OFFICIAL_PYTHON_IMAGE} as test-base-image

COPY --from=dev-dependencies-build-stage /application_root/.venv /application_root/.venv

COPY /app /application_root/app/
COPY /tests /application_root/tests/


# image for running pep8 checks
FROM test-base-image as black-test-image

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /entrypoints/black_entrypoint.sh /entrypoints/

ENTRYPOINT /entrypoints/black_entrypoint.sh $0 $@

CMD ["--target-version py39", "--check", " --line-length 80", "."]

# image for running unit tests
FROM test-base-image as unit-test-image

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /entrypoints/pytest_entrypoint.sh /entrypoints/

ENTRYPOINT /entrypoints/pytest_entrypoint.sh $0 $@

# You need to use pytest-cov as pytest plugin. Makes life very simple.
# tests directory is configured in pyproject.toml
# https://github.com/pytest-dev/pytest-cov
CMD ["--cov=app", "--cov-report=xml:/test_coverage_reports/unit_tests_coverage.xml"]
