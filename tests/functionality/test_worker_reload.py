from time import sleep
from uuid import uuid4

import pytest
from docker.models.containers import Container

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import SLEEP_TIME, EXPOSED_CONTAINER_PORT


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_worker_reload(
    docker_client,
    fast_api_multistage_development_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_development_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    )
    sleep(SLEEP_TIME)

    for number in range(1, 4):
        (exit_code, output) = test_container.exec_run(
            ["touch", "/application_root/app/main.py"]
        )
        assert exit_code == 0
        assert output.decode("utf-8") == ""
        sleep(SLEEP_TIME)

        logs: str = test_container.logs().decode("utf-8")
        logs_list: list[str] = logs.split("\n")
        log_statement_count: int = len(
            [
                line
                for line in logs_list
                if line
                == "WARNING:  WatchFiles detected changes in 'app/main.py'. Reloading..."
            ]
        )
        assert log_statement_count == number
