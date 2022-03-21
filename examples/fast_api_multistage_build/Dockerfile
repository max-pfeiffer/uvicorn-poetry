# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-poetry:1.0.1-python3.9.8-slim-bullseye
ARG OFFICIAL_PYTHON_IMAGE
FROM ${BASE_IMAGE_NAME_AND_TAG} as base-image

WORKDIR /application_root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --no-dev

FROM ${OFFICIAL_PYTHON_IMAGE} as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root

COPY --from=base-image /application_root/.venv /application_root/.venv
COPY --from=base-image /application_server/start_uvicorn.sh /application_server/start_uvicorn.sh

# This RUN statement at this place fixes an issue while running the tests with GitHub Actions.
# Tests work reliable locally on my machine or running GitHub Actions using act.
# There is a bug with multistage builds in GitHub Actions which I can also reliable reproduce
# see: https://github.com/moby/moby/issues/37965
# Will also check if I can fix that annoying issue with some tweaks to docker build args
# see: https://gist.github.com/UrsaDK/f90c9632997a70cfe2a6df2797731ac8

# Use a non-root user to run the application
# see: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN adduser --system --no-create-home python_application

COPY /app /application_root/app/

EXPOSE 80

USER python_application

CMD ["/application_server/start_uvicorn.sh"]

FROM ${OFFICIAL_PYTHON_IMAGE} as production-image-json-logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    UVICORN_LOG_CONFIG=/application_server/logging_configuration_file.yaml \
    UVICORN_LOG_LEVEL="trace"

COPY --from=base-image /application_root/.venv /application_root/.venv
COPY --from=base-image /application_server/start_uvicorn.sh /application_server/

# This RUN statement at this place fixes an issue while running the tests with GitHub Actions.
# Tests work reliable locally on my machine or running GitHub Actions using act.
# There is a bug with multistage builds in GitHub Actions which I can also reliable reproduce
# see: https://github.com/moby/moby/issues/37965
# Will also check if I can fix that annoying issue with some tweaks to docker build args
# see: https://gist.github.com/UrsaDK/f90c9632997a70cfe2a6df2797731ac8

# Use a non-root user to run the application
# see: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN adduser --system --no-create-home python_application

# Adding log configuration for Uvicorn
COPY /application_server/logging_configuration_file.yaml /application_server/logging_configuration_file.yaml

COPY /app /application_root/app/

EXPOSE 80

USER python_application

CMD ["/application_server/start_uvicorn.sh"]

FROM base-image as development-image
ENV UVICORN_RELOAD=1 \
    UVICORN_LOG_LEVEL="debug"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-interaction --no-root

COPY . /application_root/

FROM base-image as test-base-image
ENV UVICORN_LOG_LEVEL="debug"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-interaction --no-root

COPY /app /application_root/app/
COPY /tests /application_root/tests/

# image for running pep8 checks
FROM test-base-image as black-test-image

ENTRYPOINT /entrypoints/black_entrypoint.sh $0 $@

CMD ["--target-version py39", "--check", " --line-length 80", "app"]

# image for running unit tests
FROM test-base-image as unit-test-image

ENTRYPOINT /entrypoints/pytest_entrypoint.sh $0 $@

# You need to use pytest-cov as pytest plugin. Makes life very simple.
# tests directory is configured in pyproject.toml
# https://github.com/pytest-dev/pytest-cov
CMD ["--cov=app", "--cov-report=xml:/test_coverage_reports/unit_tests_coverage.xml"]
