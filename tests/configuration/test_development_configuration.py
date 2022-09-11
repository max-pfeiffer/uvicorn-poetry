import json
from time import sleep

import requests
from docker.models.containers import Container

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import (
    TEST_CONTAINER_NAME,
    SLEEP_TIME,
    HELLO_WORLD,
    DEVELOPMENT_UVICORN_CONFIG,
)
from tests.utils import UvicornPoetryContainerConfig


def verify_container_config(container: UvicornPoetryContainerConfig) -> None:
    response = requests.get("http://127.0.0.1")
    assert json.loads(response.text) == HELLO_WORLD

    config_data: dict[str, str] = container.get_uvicorn_conf()
    assert config_data["workers"] == DEVELOPMENT_UVICORN_CONFIG["workers"]
    assert config_data["host"] == DEVELOPMENT_UVICORN_CONFIG["host"]
    assert config_data["port"] == DEVELOPMENT_UVICORN_CONFIG["port"]


def test_development_configuration(
    docker_client, fast_api_multistage_development_image
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_development_image,
        name=TEST_CONTAINER_NAME,
        ports={APPLICATION_SERVER_PORT: "80"},
        detach=True,
    )
    uvicorn_gunicorn_container_config: UvicornPoetryContainerConfig = (
        UvicornPoetryContainerConfig(test_container)
    )
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container_config)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container_config)
