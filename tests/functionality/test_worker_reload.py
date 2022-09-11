import time

from docker.models.containers import Container

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME


def test_worker_reload(docker_client, images) -> None:
    test_container: Container = docker_client.containers.run(
        images.fast_api_multistage_development_image,
        name=TEST_CONTAINER_NAME,
        ports={APPLICATION_SERVER_PORT: "80"},
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
                == "WARNING:  WatchFiles detected changes in 'app/main.py'. Reloading..."
            ]
        )
        assert log_statement_count == number
