import json
from time import sleep
from uuid import uuid4

import pytest
import requests
from docker.models.containers import Container

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import (
    SLEEP_TIME,
    HELLO_WORLD,
    DEFAULT_UVICORN_CONFIG,
    EXPOSED_CONTAINER_PORT,
)
from tests.utils import UvicornPoetryContainerConfig


def verify_container_config(
    container_config: UvicornPoetryContainerConfig,
) -> None:
    response = requests.get(f"http://127.0.0.1:{EXPOSED_CONTAINER_PORT}")
    assert json.loads(response.text) == HELLO_WORLD

    config_data: dict[str, str] = container_config.get_uvicorn_conf()
    assert config_data["workers"] == DEFAULT_UVICORN_CONFIG["workers"]
    assert config_data["host"] == DEFAULT_UVICORN_CONFIG["host"]
    assert config_data["port"] == DEFAULT_UVICORN_CONFIG["port"]


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_multistage_image(
    docker_client,
    fast_api_multistage_production_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_production_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
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


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_single_stage_image(
    docker_client,
    fast_api_singlestage_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_singlestage_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
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
