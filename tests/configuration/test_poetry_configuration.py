import time

from docker.models.containers import Container

from build.constants import (
    POETRY_VERSION,
)
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


def test_poetry_configuration(docker_client, images) -> None:
    test_container: Container = docker_client.containers.run(
        images.fast_api_singlestage_image,
        name=TEST_CONTAINER_NAME,
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
