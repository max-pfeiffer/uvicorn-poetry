from random import randrange

import docker
import pytest
from docker.client import DockerClient
from semver import VersionInfo


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture(scope="session")
def version() -> str:
    version: VersionInfo = VersionInfo(
        major=randrange(100), minor=randrange(100), patch=randrange(100)
    )
    version_string: str = str(version)
    return version_string
