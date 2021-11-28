import pytest
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import VERSIONS


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
@pytest.mark.parametrize("version", VERSIONS)
def test_build_version(docker_client, target_architecture, version) -> None:
    uvicorn_gunicorn_poetry_image: Image = UvicornGunicornPoetryImage(
        docker_client
    ).build(target_architecture, version=version)
    fast_api_multistage_image: Image = FastApiMultistageImage(
        docker_client
    ).build(target_architecture, "production-image", version=version)

    assert (
        len(
            [
                tag
                for tag in uvicorn_gunicorn_poetry_image.tags
                if tag.endswith(version)
            ]
        )
        > 0
    )
    assert (
        len(
            [
                tag
                for tag in fast_api_multistage_image.tags
                if tag.endswith(version)
            ]
        )
        > 0
    )
