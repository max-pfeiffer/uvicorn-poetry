[![codecov](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry/branch/main/graph/badge.svg?token=WQI2SJJLZN)](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry)
# uvicorn-poetry
This image provides a platform to run Python applications with [Uvicorn](https://github.com/encode/uvicorn) on [Kubernetes](https://kubernetes.io/) container orchestration system.
It provides [Poetry](https://python-poetry.org/) for managing dependencies and setting up a virtual environment in the container.

This image aims to follow the best practices for a production grade container image for hosting Python web applications based
on micro frameworks like [FastAPI](https://fastapi.tiangolo.com/).
Therefore source and documentation contain a lot of references to documentation of dependencies used in this project, so users
of this image can follow up on that.

Any feedback is highly appreciated and will be considered.

Docker Hub: [pfeiffermax/uvicorn-poetry](https://hub.docker.com/r/pfeiffermax/uvicorn-poetry)

GitHub Repository: [https://github.com/max-pfeiffer/uvicorn-poetry](https://github.com/max-pfeiffer/uvicorn-poetry)
