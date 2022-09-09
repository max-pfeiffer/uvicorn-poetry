import time

import pytest
from docker.models.containers import Container
from docker.models.images import Image

from build.constants import (
    TARGET_ARCHITECTURES,
    POETRY_VERSION,
    APPLICATION_SERVER_PORT,
)
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_poetry_configuration(
    docker_client, target_architecture, version
) -> None:
    UvicornGunicornPoetryImage(docker_client).build(
        target_architecture, version=version
    )
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture,
        "production-dependencies-build-stage",
        version=version,
    )

    test_container: Container = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={APPLICATION_SERVER_PORT: "80"},
        detach=True,
    )
    time.sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run(["poetry", "--version"])
    assert exit_code == 0
    assert f"Poetry (version {POETRY_VERSION})" in output.decode("utf-8")

    (exit_code_config, output_config) = test_container.exec_run(
        ["poetry", "config", "--list"]
    )
    assert exit_code_config == 0
    assert "virtualenvs.in-project = true" in output_config.decode("utf-8")
