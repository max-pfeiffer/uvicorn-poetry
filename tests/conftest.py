from random import randrange

import docker
import pytest
from docker.models.images import Image
from semver import VersionInfo

from build.constants import (
    TARGET_ARCHITECTURES,
)
from build.images import (
    UvicornPoetryImage,
    FastApiMultistageImage,
    FastApiMultistageJsonLoggingImage,
)
from tests.utils import ImageTagComponents


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
def uvicorn_poetry_image(docker_client, version, request) -> str:
    target_architecture: str = request.param

    uvicorn_gunicorn_poetry_image: Image = UvicornPoetryImage(
        docker_client, target_architecture, version
    ).build()
    image_tag: str = uvicorn_gunicorn_poetry_image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def fast_api_multistage_image(docker_client, uvicorn_poetry_image) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_poetry_image
    )

    target: str = "production-image"
    image_version: str = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(
        docker_client, components.target_architecture, image_version
    ).build(target, uvicorn_poetry_image)
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def fast_api_multistage_with_json_logging_image(
    docker_client, uvicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_poetry_image
    )

    target: str = "production-image-with-json-logging"
    image_version: str = f"{components.version}-{target}"

    image: Image = FastApiMultistageJsonLoggingImage(
        docker_client, components.target_architecture, image_version
    ).build(
        target,
        uvicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="function")
def cleaned_up_test_container(docker_client, request) -> None:
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
