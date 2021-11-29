ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-poetry:1.0.1-python3.9.8-slim-bullseye
FROM ${BASE_IMAGE_NAME_AND_TAG} as base-image

WORKDIR /application_root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --no-dev

FROM base-image as test-base-image
ENV LOG_LEVEL="debug"

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

FROM base-image as development-image
ENV RELOAD="true" \
    LOG_LEVEL="debug"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-interaction --no-root

COPY . /application_root/

FROM base-image as production-image

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# This RUN statement fixes an issue while running the tests with GitHub Actions.
# Tests work reliable locally on my machine or running GitHub Actions using act.
# There is a bug with multistage builds in GitHub Actions which I can also reliable reproduce
# see: https://github.com/moby/moby/issues/37965
# Will also check if I can fix that annoying issue with some tweaks to docker build args
# see: https://gist.github.com/UrsaDK/f90c9632997a70cfe2a6df2797731ac8
RUN true

COPY /app /application_root/app/
