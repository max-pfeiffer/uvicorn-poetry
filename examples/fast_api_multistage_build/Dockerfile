# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE=pfeiffermax/uvicorn-poetry:3.0.0-python3.10.9-slim-bullseye@sha256:cdd772b5e6e3f2feb8d38f3ca7af9b955c886a86a4aecec99bc43897edd8bcbe
FROM ${BASE_IMAGE} as dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${BASE_IMAGE} as production-image

# Copy virtual environment
COPY --chown=python_application:python_application --from=dependencies-build-stage /application_root/.venv /application_root/.venv

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/
