"""Test fixtures."""

from os import getenv
from random import randrange

import pytest
from python_on_whales import Builder, DockerClient
from semver import VersionInfo


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    """Fixture provides a Python-on-Whales docker client.

    :return:
    """
    return DockerClient(debug=True)


@pytest.fixture(scope="session")
def pow_buildx_builder(docker_client: DockerClient) -> Builder:
    """Fixture for providing a Python-on-Whales buildx builder.

    :param docker_client:
    :return:
    """
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )
    yield builder
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


@pytest.fixture(scope="session")
def image_version() -> str:
    """Fixture providing a fake image version.

    :return:
    """
    version: VersionInfo = VersionInfo(
        major=randrange(100), minor=randrange(100), patch=randrange(100)
    )
    version_string: str = str(version)
    return version_string


@pytest.fixture(scope="session")
def python_version() -> str:
    """Fixture provides the Python version set in .env file.

    :return:
    """
    return getenv("PYTHON_VERSION")


@pytest.fixture(scope="session")
def os_variant() -> str:
    """Fixture provides the OS variant set in .env file.

    :return:
    """
    return getenv("OS_VARIANT")
