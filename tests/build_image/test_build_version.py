import pytest

from build.constants import (
    TARGET_ARCHITECTURES,
)
from build.images import (
    UvicornPoetryImage,
    FastApiMultistageImage,
    FastApiMultistageJsonLoggingImage,
)
from tests.utils import ImageTagComponents


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_image_versions(target_architecture, version, docker_client):
    uvicorn_poetry_image_object: UvicornPoetryImage = UvicornPoetryImage(
        docker_client, target_architecture, version
    )
    assert (
        uvicorn_poetry_image_object.target_architecture == target_architecture
    )
    assert uvicorn_poetry_image_object.version == version

    fastapi_multistage_imageobject: FastApiMultistageImage = (
        FastApiMultistageImage(docker_client, target_architecture, version)
    )
    assert (
        fastapi_multistage_imageobject.target_architecture
        == target_architecture
    )
    assert fastapi_multistage_imageobject.version == version

    fastapi_multistage_jsonlogging_imageobject: FastApiMultistageJsonLoggingImage = FastApiMultistageJsonLoggingImage(
        docker_client, target_architecture, version
    )
    assert (
        fastapi_multistage_jsonlogging_imageobject.target_architecture
        == target_architecture
    )
    assert fastapi_multistage_jsonlogging_imageobject.version == version


def test_build_version(uvicorn_poetry_image, version) -> None:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_poetry_image
    )
    assert components.version == version
