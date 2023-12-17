from click.testing import CliRunner, Result
from python_on_whales import DockerException

from build.publish import main
from tests.constants import REGISTRY_USERNAME, REGISTRY_PASSWORD
from tests.registry_container import DockerRegistryContainer


def test_registry_with_credentials(
    cli_runner: CliRunner,
    image_version: str,
    python_version: str,
    os_variant: str,
):
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            env={
                "DOCKER_HUB_USERNAME": REGISTRY_USERNAME,
                "DOCKER_HUB_PASSWORD": REGISTRY_PASSWORD,
                "GIT_TAG_NAME": image_version,
                "PYTHON_VERSION": python_version,
                "OS_VARIANT": os_variant,
                "REGISTRY": docker_registry.get_registry(),
            },
        )
        assert result.exit_code == 0


def test_registry_with_wrong_credentials(
    cli_runner: CliRunner,
    image_version: str,
    python_version: str,
    os_variant: str,
):
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            env={
                "DOCKER_HUB_USERNAME": "boom",
                "DOCKER_HUB_PASSWORD": "bang",
                "GIT_TAG_NAME": image_version,
                "PYTHON_VERSION": python_version,
                "OS_VARIANT": os_variant,
                "REGISTRY": docker_registry.get_registry(),
            },
        )
        assert result.exit_code == 1
        assert isinstance(result.exception, DockerException)
