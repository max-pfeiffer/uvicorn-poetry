import json
from time import sleep

import requests
from python_on_whales import DockerClient

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import (
    DEFAULT_UVICORN_CONFIG,
    EXPOSED_CONTAINER_PORT,
    HELLO_WORLD,
    SLEEP_TIME,
)
from tests.utils import UvicornPoetryContainerConfig


def test_fast_api_multistage_with_json_logging_image(
    docker_client: DockerClient,
    fast_api_multistage_with_json_logging_image_reference: str,
) -> None:
    with docker_client.container.run(
        fast_api_multistage_with_json_logging_image_reference,
        detach=True,
        publish=[(EXPOSED_CONTAINER_PORT, APPLICATION_SERVER_PORT)],
    ) as container:
        # Wait for uvicorn to come up
        sleep(SLEEP_TIME)

        uvicorn_gunicorn_container_config: UvicornPoetryContainerConfig = (
            UvicornPoetryContainerConfig(container.id)
        )

        assert (
            f"{APPLICATION_SERVER_PORT}/tcp"
            in container.config.exposed_ports.keys()
        )

        response = requests.get(f"http://127.0.0.1:{EXPOSED_CONTAINER_PORT}")
        assert json.loads(response.text) == HELLO_WORLD

        config_data: dict[
            str, str
        ] = uvicorn_gunicorn_container_config.get_uvicorn_conf()
        assert config_data["workers"] == DEFAULT_UVICORN_CONFIG["workers"]
        assert config_data["host"] == DEFAULT_UVICORN_CONFIG["host"]
        assert config_data["port"] == DEFAULT_UVICORN_CONFIG["port"]

        logs: str = container.logs()
        lines: list[str] = logs.splitlines()
        log_statement: dict = json.loads(lines[1])
        assert log_statement["levelname"] == "INFO"
