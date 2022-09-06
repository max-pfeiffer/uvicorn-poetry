import json
import time

import pytest
import requests
from docker.models.containers import Container
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES, APPLICATION_SERVER_PORT
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import (
    TEST_CONTAINER_NAME,
    SLEEP_TIME,
    HELLO_WORLD,
    DEVELOPMENT_UVICORN_CONFIG,
)
from tests.utils import UvicornGunicornPoetryContainerConfig


def verify_container(container: UvicornGunicornPoetryContainerConfig) -> None:
    response = requests.get("http://127.0.0.1")
    assert json.loads(response.text) == HELLO_WORLD

    config_data: dict[str, str] = container.get_uvicorn_conf()
    assert config_data["workers"] == DEVELOPMENT_UVICORN_CONFIG["workers"]
    assert config_data["host"] == DEVELOPMENT_UVICORN_CONFIG["host"]
    assert config_data["port"] == DEVELOPMENT_UVICORN_CONFIG["port"]


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_default_configuration(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "development-image"
    )

    test_container: Container = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={APPLICATION_SERVER_PORT: "80"},
        detach=True,
    )
    uvicorn_gunicorn_container: UvicornGunicornPoetryContainerConfig = (
        UvicornGunicornPoetryContainerConfig(test_container)
    )
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
