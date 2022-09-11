from time import sleep

from docker.models.containers import Container

from build.constants import (
    PYTHON_VERSIONS,
)
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME
from tests.utils import ImageTagComponents


def test_python_version(
    docker_client, fast_api_multistage_production_image
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_production_image,
        name=TEST_CONTAINER_NAME,
        detach=True,
    )
    sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run(["python", "--version"])
    assert exit_code == 0

    components: ImageTagComponents = ImageTagComponents.create_from_tag(
        fast_api_multistage_production_image
    )

    version_string: str = (
        f"Python {PYTHON_VERSIONS[components.target_architecture]}"
    )
    assert version_string in output.decode("utf-8")
