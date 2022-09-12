from tests.utils import ImageTagComponents


def test_build_version(uvicorn_gunicorn_poetry_image, version) -> None:
    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        uvicorn_gunicorn_poetry_image
    )
    assert components.version == version
