#!/bin/bash

 docker image build --build-arg OFFICIAL_PYTHON_IMAGE=python:3.9.13-bullseye --build-arg IMAGE_POETRY_VERSION=1.2.0 --build-arg APPLICATION_SERVER_PORT=80 --tag uvicorn-poetry:test .
