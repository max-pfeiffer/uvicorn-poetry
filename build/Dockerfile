# Base image: https://hub.docker.com/r/pfeiffermax/python-poetry
# Dockerfile: https://github.com/max-pfeiffer/python-poetry/blob/main/build/Dockerfile
ARG BASE_IMAGE
ARG APPLICATION_SERVER_PORT
FROM ${BASE_IMAGE}

LABEL maintainer="Max Pfeiffer <max@maxpfeiffer.ch>"

# References:
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# https://pip.pypa.io/en/stable/topics/caching/#avoiding-caching
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_NO_CACHE_DIR#cmdoption-no-cache-dir
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DISABLE_PIP_VERSION_CHECK#cmdoption-disable-pip-version-check
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DEFAULT_TIMEOUT#cmdoption-timeout
# https://pip.pypa.io/en/stable/topics/configuration/#environment-variables
# https://python-poetry.org/docs/#installation

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    VIRTUAL_ENVIRONMENT_PATH="/application_root/.venv"

ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Set the WORKDIR to the application root. This needed for the entrypoints to
# work. Also Uvicorn --reload feature relies by default on the current work dir.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}

COPY ./scripts/start_uvicorn.sh /application_server/
RUN chmod +x /application_server/start_uvicorn.sh

COPY ./scripts/pytest_entrypoint.sh ./scripts/black_entrypoint.sh /entrypoints/
RUN chmod +x /entrypoints/pytest_entrypoint.sh
RUN chmod +x /entrypoints/black_entrypoint.sh

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_uvicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}
