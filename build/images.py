import os
from datetime import datetime
from typing import Dict

import docker
from docker.models.images import Image

from build.constants import (
    UVICORN_GUNICORN_POETRY_IMAGE_NAME,
    BASE_IMAGES,
    FAST_API_MULTISTAGE_IMAGE_NAME,
)


class DockerImage:
    def __init__(self, docker_client: docker.client):
        self.docker_client: docker.client = docker_client
        self.absolute_package_directory_path: str = os.path.dirname(
            os.path.abspath(__file__)
        )
        self.image_name: str = None
        self.image_tag: str = None
        self.version_tag: str = datetime.today().strftime("%Y-%m-%d")
        self.dockerfile_name: str = "Dockerfile"


class UvicornGunicornPoetryImage(DockerImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        self.absolute_docker_image_directory_path: str = (
            self.absolute_package_directory_path
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        # self.image_name = 'pfeiffermax/uvicorn-gunicorn-poetry'
        self.image_name = UVICORN_GUNICORN_POETRY_IMAGE_NAME

    def build(self, target_architecture: str, version: str = None) -> Image:
        if version is not None:
            self.version_tag = version

        buildargs: Dict[str, str] = {
            "OFFICIAL_PYTHON_IMAGE": BASE_IMAGES[target_architecture]
        }
        tag: str = f"{self.image_name}:{self.version_tag}-{target_architecture}"

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile=self.dockerfile_name,
            tag=tag,
            buildargs=buildargs,
        )[0]
        return image


class FastApiMultistageImage(DockerImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        absolute_project_root_directory: str = os.path.split(
            self.absolute_package_directory_path
        )[0]
        self.absolute_docker_image_directory_path: str = os.path.join(
            absolute_project_root_directory,
            "examples/fast_api_multistage_build",
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = FAST_API_MULTISTAGE_IMAGE_NAME

    def build(
        self, target_architecture: str, target: str, version: str = None
    ) -> Image:
        if version is not None:
            self.version_tag = version

        self.image_tag = f"{self.version_tag}-{target_architecture}"

        buildargs: Dict[str, str] = {
            "BASE_IMAGE_NAME_AND_TAG": f"{UVICORN_GUNICORN_POETRY_IMAGE_NAME}:{self.image_tag}"
        }
        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            target=target,
            buildargs=buildargs,
        )[0]
        return image
