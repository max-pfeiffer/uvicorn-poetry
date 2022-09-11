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
from tests.utils import ImageTagComponents, \
    create_version_tag_for_example_images


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
def uvicorn_gunicorn_poetry_image(docker_client, version, request) -> str:
    target_architecture: str = request.param

    uvicorn_gunicorn_poetry_image: Image = UvicornGunicornPoetryImage(
        docker_client
    ).build(target_architecture, version=version)
    image_tag: str = uvicorn_gunicorn_poetry_image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_multistage_production_image(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    target: str = "production-image"
    image_version = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(docker_client).build(
        components.target_architecture,
        target,
        image_version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_multistage_production_image_json_logging(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    target: str = "production-image-json-logging"
    image_version = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(docker_client).build(
        components.target_architecture,
        target,
        image_version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_multistage_development_image(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    target: str = "development-image"
    image_version = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(docker_client).build(
        components.target_architecture,
        target,
        image_version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_multistage_development_black_test_image(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    target: str = "black-test-image"
    image_version = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(docker_client).build(
        components.target_architecture,
        target,
        image_version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_multistage_development_unit_test_image(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    target: str = "unit-test-image"
    image_version = f"{components.version}-{target}"

    image: Image = FastApiMultistageImage(docker_client).build(
        components.target_architecture,
        target,
        image_version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


@pytest.fixture(scope="session")
def fast_api_singlestage_image(
    docker_client, uvicorn_gunicorn_poetry_image
) -> str:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )

    image: Image = FastApiSinglestageImage(docker_client).build(
        components.target_architecture,
        components.version,
        uvicorn_gunicorn_poetry_image,
    )
    image_tag: str = image.tags[0]
    return image_tag


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
