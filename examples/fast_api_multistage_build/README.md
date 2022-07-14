# fast-api-multistage-build
This is an example project to demonstrate the use of the uvicorn-poetry image.
It is also used for testing that image.

## App module discovery
Poetry does add your project's root directory already to sys.path. You can check this with:
```shell
python -m site
```
In uvicorn-poetry container's Dockerfile PYTHONPATH is set, so this is cared for already when building containers
upon that image.

## Tests
When running the project locally and not inside of a container please be aware that
you don't need to run
[pytest over the Pyton interpreter](https://docs.pytest.org/en/6.2.x/goodpractices.html#tests-outside-application-code).
Instead you can just run pytest like that:
```shell
pytest
```

## Custom log config
Please be aware of [Uvicorn's default logging config](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py).
I took that basically as a template for the custom logging config which I provided as an example for demonstrating
the use of this configuration option and the environment variable. I choose the JSON formatter for customisation because
this is a common use case when you run your application on Kubernetes with a log aggregation system. 
Please be aware that there are more convenient options to achieve this like with the
[json-logging-python package](https://github.com/bobbui/json-logging-python).
