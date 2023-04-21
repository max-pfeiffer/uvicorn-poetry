from click.testing import CliRunner, Result
from docker.errors import APIError

from build.publish import main
from tests.constants import REGISTRY_USERNAME, REGISTRY_PASSWORD
from tests.registry_container import DockerRegistryContainer
import pytest


@pytest.mark.usefixtures("cleanup_images")
def test_registry(cli_runner: CliRunner, version: str):
    with DockerRegistryContainer().with_bind_ports(
        5000, 5000
    ) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--version-tag",
                version,
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 0


@pytest.mark.usefixtures("cleanup_images")
def test_registry_with_unnecessary_credentials(
    cli_runner: CliRunner, version: str
):
    with DockerRegistryContainer().with_bind_ports(
        5000, 5000
    ) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--docker-hub-username",
                "bang",
                "--docker-hub-password",
                "boom",
                "--version-tag",
                version,
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 0


@pytest.mark.usefixtures("cleanup_images")
def test_registry_with_credentials(cli_runner: CliRunner, version: str):
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--docker-hub-username",
                REGISTRY_USERNAME,
                "--docker-hub-password",
                REGISTRY_PASSWORD,
                "--version-tag",
                version,
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 0


@pytest.mark.usefixtures("cleanup_images")
def test_registry_with_wrong_credentials(cli_runner: CliRunner, version: str):
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--docker-hub-username",
                "bang",
                "--docker-hub-password",
                "boom",
                "--version-tag",
                version,
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 1
        assert isinstance(result.exception, APIError)
