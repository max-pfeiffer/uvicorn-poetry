from uuid import uuid4

import docker
import pytest
from docker.errors import NotFound

from build.constants import (
    UVICORN_POETRY_IMAGE_NAME,
    FAST_API_MULTISTAGE_IMAGE_NAME,
    FAST_API_SINGLESTAGE_IMAGE_NAME,
)
from tests.constants import TEST_CONTAINER_NAME


@pytest.fixture(scope="session")
def docker_client() -> docker.client:
    return docker.client.from_env()


@pytest.fixture(scope="function")
def version() -> str:
    return str(uuid4())


@pytest.fixture(scope="function", autouse=True)
def prepare_docker_env(docker_client) -> None:
    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
    # Delete old existing images
    for old_image in docker_client.images.list(UVICORN_POETRY_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    for old_image in docker_client.images.list(FAST_API_SINGLESTAGE_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    for old_image in docker_client.images.list(FAST_API_MULTISTAGE_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)

    yield None

    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
    # Delete old existing images
    for old_image in docker_client.images.list(UVICORN_POETRY_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    for old_image in docker_client.images.list(FAST_API_SINGLESTAGE_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    for old_image in docker_client.images.list(FAST_API_MULTISTAGE_IMAGE_NAME):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
