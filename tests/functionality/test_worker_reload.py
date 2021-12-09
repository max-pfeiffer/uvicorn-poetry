import time

import pytest
from docker.models.containers import Container
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_worker_reload(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "development-image"
    )

    test_container: Container = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    )
    time.sleep(SLEEP_TIME)

    for number in range(1, 4):
        (exit_code, output) = test_container.exec_run(
            ["touch", "/application_root/app/main.py"]
        )
        assert exit_code == 0
        assert output.decode("utf-8") == ""
        time.sleep(SLEEP_TIME)

        logs: str = test_container.logs().decode("utf-8")
        logs_list: list[str] = logs.split("\n")
        log_statement_count: int = len(
            [
                line
                for line in logs_list
                if line
                == "WARNING:  WatchGodReload detected file change in '['/application_root/app/main.py']'. Reloading..."
            ]
        )
        assert log_statement_count == number
