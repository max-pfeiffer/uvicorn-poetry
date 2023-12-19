# fast-api-multistage-build
This is an example project to demonstrate the use of the uvicorn-poetry image.
It is also used for testing that image.

## Build the image
```shell
docker build --tag fast-api-singlestage .
```
Build the image with another base image variant:
```shell
docker build --build-arg BASE_IMAGE=pfeiffermax/uvicorn-poetry:3.2.0-python3.10.13-bookworm --tag fast-api-singlestage .
```

## Run the image
```shell
docker run -it --rm fast-api-singlestage
```
