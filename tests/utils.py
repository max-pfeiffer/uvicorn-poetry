"""Utilities for tests."""

from dataclasses import dataclass
from pathlib import Path

import docker
from docker.models.containers import Container
from docker_image import reference


class UvicornPoetryContainerConfig:
    """Class for providing container configuration."""

    def __init__(self, container_id: str):
        """Class initializer.

        :param container_id:
        """
        self.container: Container = docker.from_env().containers.get(container_id)

    def get_uvicorn_processes(self) -> list[str]:
        """Return uvicorn processes.

        :return:
        """
        top = self.container.top()
        process_commands: list[str] = [p[7] for p in top["Processes"]]
        uvicorn_processes: list[str] = [
            p for p in process_commands if "/application_root/.venv/bin/uvicorn" in p
        ]
        return uvicorn_processes

    def get_uvicorn_conf(self) -> dict[str, any]:
        """Return uvicorn configuration.

        :return:
        """
        uvicorn_config: dict[str, any] = {}
        uvicorn_processes = self.get_uvicorn_processes()
        first_process = uvicorn_processes[0]

        first_part: str
        partition: str
        last_part: str
        first_part, partition, last_part = first_process.partition(
            "/application_root/.venv/bin/uvicorn"
        )

        uvicorn_arguments: list[str] = last_part.strip().split()
        app: str = uvicorn_arguments.pop()
        uvicorn_config["app"] = app

        for index, element in enumerate(uvicorn_arguments):
            option: str
            value: any
            if element.startswith("--"):
                option = element.lstrip("--")
                try:
                    next_element = uvicorn_arguments[index + 1]
                    if next_element.startswith("--"):
                        # It is an option without value
                        value = True
                    else:
                        # add the value for the current option
                        value = next_element
                except IndexError:
                    # It is an option without value at the end of options list
                    value = True

            uvicorn_config[option] = value
        return uvicorn_config


@dataclass
class ImageTagComponents:
    """Class for parsing and providing image tag components."""

    registry: str
    image_name: str
    tag: str
    version: str
    python_version: str
    os_variant: str

    @classmethod
    def create_from_reference(cls, tag: str):
        """Instantiate a class using an image tag.

        :param tag:
        :return:
        """
        ref = reference.Reference.parse(tag)
        registry: str = ref.repository["domain"]
        image_name: str = ref.repository["path"]
        tag: str = ref["tag"]

        tag_parts: list[str] = tag.split("-")
        version: str = tag_parts[0]
        python_version: str = tag_parts[1].lstrip("python")
        os_variant: str = "-".join(tag_parts[2:])
        return cls(
            registry=registry,
            image_name=image_name,
            tag=tag,
            version=version,
            python_version=python_version,
            os_variant=os_variant,
        )


def get_fast_api_singlestage_context() -> Path:
    """Return Docker build context for single stage example app.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_singlestage_build"
    )
    return context


def get_fast_api_singlestage_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for single stage example app.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast-api-singlestage-build:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference


def get_fast_api_multistage_context() -> Path:
    """Return Docker build context for multi-stage example app.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_multistage_build"
    )
    return context


def get_fast_api_multistage_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for multi-stage example app.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast-api-multistage-build:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference


def get_fast_api_multistage_with_json_logging_context() -> Path:
    """Return Docker build context for multi-stage example app with JSON logging.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_multistage_build_with_json_logging"
    )
    return context


def get_fast_api_multistage_with_json_logging_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for multi-stage example app with JSON logging.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast_api_multistage_build_with_json_logging:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference
