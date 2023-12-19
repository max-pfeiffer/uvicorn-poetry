# fast-api-multistage-build-with-json-logging
This is an example project to demonstrate the use of the uvicorn-poetry image.
It is also used for testing that image.

## Custom log config
Please be aware of [Uvicorn's default logging config](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py).
I took that basically as a template for the custom logging config which I provided as an example for demonstrating
the use of this configuration option and the environment variable. I choose the JSON formatter for customisation because
this is a common use case when you run your application on Kubernetes with a log aggregation system. 
Please be aware that there are more convenient options to achieve this like with the
[json-logging-python package](https://github.com/bobbui/json-logging-python).

## Build the image
```shell
docker build --tag fast-api-multistage --target production-image .
```
Build the image with another base image variant:
```shell
docker build --build-arg BASE_IMAGE=pfeiffermax/uvicorn-poetry:3.2.0-python3.10.13-bookworm --tag fast-api-multistage --target production-image .
```

## Run the image
```shell
docker run -it --rm fast-api-multistage
```
