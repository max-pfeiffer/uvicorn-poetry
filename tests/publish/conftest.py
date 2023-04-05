import pytest
from click.testing import CliRunner
from docker.client import DockerClient


@pytest.fixture(scope="package")
def cli_runner() -> CliRunner:
    runner = CliRunner()
    return runner


@pytest.fixture(scope="package")
def cleanup_images(docker_client: DockerClient):
    yield
    for old_image in docker_client.images.list("pfeiffermax/uvicorn-poetry"):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
