#!/bin/bash

docker build --build-arg BASE_IMAGE_NAME_AND_TAG=uvicorn-poetry:test --build-arg OFFICIAL_PYTHON_IMAGE=python:3.9.13-bullseye --build-arg APPLICATION_SERVER_PORT=80 --target production-image-json-logging --tag uvicorn-poetry-json:test .
