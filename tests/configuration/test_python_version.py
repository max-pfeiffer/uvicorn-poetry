from time import sleep

from docker.models.containers import Container

from build.constants import (
    PYTHON_VERSIONS,
)
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


def test_python_version(docker_client, images) -> None:
    image_tag: str = images.fast_api_multistage_production_image
    test_container: Container = docker_client.containers.run(
        image_tag,
        name=TEST_CONTAINER_NAME,
        detach=True,
    )
    sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run(["python", "--version"])
    assert exit_code == 0

    image_tag_parts: list[str] = image_tag.split(":")[-1].split("-", maxsplit=1)
    target_architecture: str = image_tag_parts[-1]
    version_string: str = f"Python {PYTHON_VERSIONS[target_architecture]}"
    assert version_string in output.decode("utf-8")
