import time

import pytest
from docker.models.containers import Container
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES, PYTHON_VERSIONS
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_python_version(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "production-image"
    )

    test_container: Container = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    )
    time.sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run(["python", "--version"])
    assert exit_code == 0

    version_string: str = f"Python {PYTHON_VERSIONS[target_architecture]}"
    assert version_string in output.decode("utf-8")
