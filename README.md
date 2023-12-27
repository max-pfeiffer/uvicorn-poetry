[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry/branch/main/graph/badge.svg?token=WQI2SJJLZN)](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry)
![pipeline workflow](https://github.com/max-pfeiffer/uvicorn-poetry/actions/workflows/pipeline.yml/badge.svg)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/pfeiffermax/uvicorn-poetry?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/pfeiffermax/uvicorn-poetry)
# uvicorn-poetry - Docker image for FastAPI
This Docker image provides a platform to run Python applications with [Uvicorn](https://github.com/encode/uvicorn) on [Kubernetes](https://kubernetes.io/) container orchestration system.
It provides [Poetry](https://python-poetry.org/) for managing dependencies and setting up a virtual environment in the container.

This image aims to follow the best practices for a production grade container image for hosting Python web applications based
on micro frameworks like [FastAPI](https://fastapi.tiangolo.com/).
Therefore, source and documentation contain a lot of references to documentation of dependencies used in this project, so users
of this image can follow up on that.

Any feedback is highly appreciated and will be considered.

**Docker Hub:** [pfeiffermax/uvicorn-poetry](https://hub.docker.com/r/pfeiffermax/uvicorn-poetry)

**GitHub Repository:** [https://github.com/max-pfeiffer/uvicorn-poetry](https://github.com/max-pfeiffer/uvicorn-poetry)

## Docker Image Features
1. Poetry v1.7.1 is available as Python package dependency management tool
2. A virtual environment for the application and application server
3. The application is run with [Uvicorn](https://www.uvicorn.org) as application server
4. Python versions:
    1. 3.10
    2. 3.11
    3. 3.12
5. Operating system variants:
    1. [Debian Bookworm v12.1](https://www.debian.org/releases/bookworm/)
    2. [Debian Bookworm slim v12.1](https://www.debian.org/releases/bookworm/)
6. Supported CPU architectures:    
   1. linux/amd64
   2. linux/arm64/v8

## Usage
The image provides a platform to run your Python application, so it does not provide an application itself.

Please have a look at the [single stage](https://github.com/max-pfeiffer/uvicorn-poetry/tree/main/examples/fast_api_singlestage_build) and [multi stage](https://github.com/max-pfeiffer/uvicorn-poetry/tree/main/examples/fast_api_multistage_build) example to learn how to use the image.

The [multi stage approach](https://github.com/max-pfeiffer/uvicorn-poetry/tree/main/examples/fast_api_multistage_build)
is a bit more efficient with regard to build time. It caches the Python package dependencies in a separate build stage.

You can also use the [uvicorn-poetry-fastapi-project-template](https://github.com/max-pfeiffer/uvicorn-poetry-fastapi-project-template) for your convenience (requires [Cookiecutter](https://github.com/cookiecutter/cookiecutter)). The generated project basically contains the Dockerfile of this image and production image is build upon the standard Python image which results in an even smaller image size eventually.

Please be aware that your application needs an application layout without src folder which is proposed in
[fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app).
The application and test structure needs to be like that:
```bash
├── .dockerignore
├── Dockerfile
├── app
│    ├── __init__.py
│    └── main.py
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    ├── conftest.py
    └── test_api
        ├── __init__.py
        ├── test_items.py
        └── test_root.py
```
Please be aware that you need to provide a pyproject.toml file to specify your Python package dependencies for Poetry and configure
dependencies like Pytest. Poetry dependencies must at least contain the following to work:
* python = "^3.11"
* uvicorn = "0.24.0"

If your application uses FastAPI framework this needs to be added as well:
* fastapi = "0.104.1"

**IMPORTANT:** make sure you have a [.dockerignore file](https://github.com/max-pfeiffer/uvicorn-poetry/blob/main/examples/fast_api_multistage_build/.dockerignore)
in your application root which excludes your local virtual environment in .venv! Otherwise you will have an issue activating that virtual
environment when running the container.

## Configuration
Configuration is done through command line options and arguments in the
[Dockerfile](https://github.com/max-pfeiffer/uvicorn-poetry/blob/main/build/Dockerfile).
For everything else Uvicorn uses its defaults.
Since [Uvicorn v0.16.0](https://github.com/encode/uvicorn/releases/tag/0.16.0) you can configure Uvicorn via
[environment variables](https://www.uvicorn.org/settings/) with the prefix `UVICORN_`.
If you would like to do a deep dive on all the configuration options please see the
[official Uvicorn documentation](https://www.uvicorn.org/settings/).

### Important changes since V3.0.0
1. Scripts for entrypoints are dropped and removed
2. Application is run with an unprivileged user

### Important change since V2.0.0
These custom environment variables are not supported anymore: 
1. `LOG_LEVEL` : The granularity of Error log outputs.
2. `LOG_CONFIG_FILE` : Logging configuration file.
3. `RELOAD` : Enable auto-reload.
