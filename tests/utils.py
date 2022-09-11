from dataclasses import dataclass

from docker.models.containers import Container


class UvicornGunicornPoetryContainerConfig:
    def __init__(self, container: Container):
        self.container: Container = container

    def get_uvicorn_processes(self) -> list[str]:
        top = self.container.top()
        process_commands: list[str] = [p[7] for p in top["Processes"]]
        uvicorn_processes: list[str] = [
            p
            for p in process_commands
            if "/application_root/.venv/bin/uvicorn" in p
        ]
        return uvicorn_processes

    def get_uvicorn_conf(self) -> dict[str, any]:
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
    image_name: str
    version: str
    target_architecture: str


def strip_docker_tag(docker_tag: str):
    image_name: str = docker_tag.split(":")[0]
    image_tag: str = docker_tag.split(":")[1]
    image_tag_parts: list[str] = image_tag.split("-", maxsplit=1)
    version: str = image_tag_parts[0]
    target_architecture: str = image_tag_parts[1]
    return ImageTagComponents(image_name=image_name, version=version, target_architecture=target_architecture)
