from random import randrange

import docker
import pytest
from docker.errors import NotFound
from docker.models.images import Image
from semver import VersionInfo

from build.constants import (
    UVICORN_POETRY_IMAGE_NAME,
    FAST_API_MULTISTAGE_IMAGE_NAME,
    FAST_API_SINGLESTAGE_IMAGE_NAME,
    TARGET_ARCHITECTURES,
)
from build.images import (
    UvicornGunicornPoetryImage,
    FastApiMultistageImage,
    FastApiSinglestageImage,
)
from tests.constants import TEST_CONTAINER_NAME
from tests.utils import ImageTags


@pytest.fixture(scope="session")
def docker_client() -> docker.client:
    return docker.client.from_env()


@pytest.fixture(scope="session")
def version() -> str:
    version: VersionInfo = VersionInfo(
        major=randrange(100), minor=randrange(100), patch=randrange(100)
    )
    version_string: str = str(version)
    return version_string


@pytest.fixture(scope="session", params=TARGET_ARCHITECTURES)
def images(docker_client, version, request) -> ImageTags:
    target_architecture: str = request.param

    uvicorn_gunicorn_poetry_image: Image = UvicornGunicornPoetryImage(
        docker_client
    ).build(target_architecture, version=version)

    fast_api_multistage_production_image: Image = FastApiMultistageImage(
        docker_client
    ).build(target_architecture, "production-image", version=version)

    fast_api_multistage_production_image_json_logging: Image = (
        FastApiMultistageImage(docker_client).build(
            target_architecture,
            "production-image-json-logging",
            version=version,
        )
    )

    fast_api_multistage_development_image: Image = FastApiMultistageImage(
        docker_client
    ).build(target_architecture, "development-image", version=version)

    fast_api_singlestage_image: Image = FastApiSinglestageImage(
        docker_client
    ).build(
        target_architecture,
        version=version,
    )

    image_tags = ImageTags(
        uvicorn_gunicorn_poetry_image=uvicorn_gunicorn_poetry_image.tags[0],
        fast_api_multistage_production_image=fast_api_multistage_production_image.tags[
            0
        ],
        fast_api_multistage_production_image_json_logging=fast_api_multistage_production_image_json_logging.tags[
            0
        ],
        fast_api_multistage_development_image=fast_api_multistage_development_image.tags[
            0
        ],
        fast_api_singlestage_image=fast_api_singlestage_image.tags[0],
    )
    return image_tags


@pytest.fixture(scope="function", autouse=True)
def prepare_docker_env_for_test_execution(docker_client) -> None:
    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass

    yield None

    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass


@pytest.fixture(scope="session", autouse=True)
def prepare_docker_env(docker_client) -> None:
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
