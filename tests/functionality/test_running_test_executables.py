from typing import Dict

import pytest
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_running_pep8_test_image(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "black-test-image"
    )

    api_response: Dict = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_running_unit_test_image(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "unit-test-image"
    )

    api_response: Dict = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0
