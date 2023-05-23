import pytest
from docker.client import DockerClient
from docker.models.images import Image
from semver import VersionInfo

from build.constants import TARGET_ARCHITECTURES
from build.images import (
    FastApiMultistageImage,
    FastApiMultistageJsonLoggingImage,
    UvicornPoetryImage,
)
from tests.utils import ImageTagComponents


@pytest.fixture(scope="package", params=TARGET_ARCHITECTURES)
def uvicorn_poetry_image(
    docker_client: DockerClient, version: str, request
) -> str:
    target_architecture: str = request.param

    uvicorn_gunicorn_poetry_image: Image = UvicornPoetryImage(
        docker_client, target_architecture, version
    ).build()
    image_tag: str = uvicorn_gunicorn_poetry_image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="package")
def fast_api_multistage_image(
    docker_client: DockerClient, uvicorn_poetry_image: str
) -> str:
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


@pytest.fixture(scope="package")
def fast_api_multistage_with_json_logging_image(
    docker_client: DockerClient, uvicorn_poetry_image: str
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
def cleaned_up_test_container(docker_client: DockerClient, request) -> None:
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
