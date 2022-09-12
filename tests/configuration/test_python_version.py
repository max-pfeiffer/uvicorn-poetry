from time import sleep
from uuid import uuid4

import pytest
from docker.models.containers import Container

from build.constants import (
    PYTHON_VERSIONS,
)
from tests.constants import SLEEP_TIME
from tests.utils import ImageTagComponents


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_python_version(
    docker_client,
    fast_api_multistage_production_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_production_image,
        name=cleaned_up_test_container,
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
