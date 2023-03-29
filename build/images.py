from pathlib import Path
from typing import Optional

import docker
from docker.models.images import Image

from build.constants import (
    BASE_IMAGES,
    APPLICATION_SERVER_PORT,
)


class DockerImage:
    def __init__(self, docker_client: docker.client):
        self.docker_client: docker.client = docker_client
        self.dockerfile_name: str = "Dockerfile"
        self.dockerfile_directory: Optional[Path] = None
        self.image_name: Optional[str] = None
        self.image_tag: Optional[str] = None
        self.version_tag: Optional[str] = None


class UvicornPoetryImage(DockerImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        # An image name is made up of slash-separated name components,
        # optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = "pfeiffermax/uvicorn-poetry"
        self.dockerfile_directory: Path = Path(__file__).parent.resolve()

    def build(self, target_architecture: str, version: str = None) -> Image:
        self.version_tag = version
        self.image_tag: str = (
            f"{self.image_name}:{self.version_tag}-{target_architecture}"
        )

        buildargs: dict[str, str] = {
            "BASE_IMAGE": BASE_IMAGES[target_architecture],
            "APPLICATION_SERVER_PORT": APPLICATION_SERVER_PORT,
        }

        image: Image = self.docker_client.images.build(
            path=str(self.dockerfile_directory),
            dockerfile=self.dockerfile_name,
            tag=self.image_tag,
            buildargs=buildargs,
        )[0]
        return image


class ExampleApplicationImage(DockerImage):
    def build(
        self,
        target_architecture: str,
        target: str,
        version: str,
        base_image_tag: str,
    ) -> Image:
        self.version_tag = version
        self.image_tag = f"{self.version_tag}-{target_architecture}"

        buildargs: dict[str, str] = {
            "BASE_IMAGE": base_image_tag,
        }
        image: Image = self.docker_client.images.build(
            path=str(self.dockerfile_directory),
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            target=target,
            buildargs=buildargs,
        )[0]
        return image


class FastApiMultistageImage(ExampleApplicationImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        # An image name is made up of slash-separated name components,
        # optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = "fast-api-multistage-build"
        self.dockerfile_directory: Path = (
            Path(__file__).parent.parent.resolve()
            / "examples"
            / "fast_api_multistage_build"
        )


class FastApiMultistageJsonLoggingImage(ExampleApplicationImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        # An image name is made up of slash-separated name components,
        # optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = "fast-api-multistage-build-with-json-logging"
        self.dockerfile_directory: Path = (
            Path(__file__).parent.parent.resolve()
            / "examples"
            / "fast_api_multistage_build_with_json_logging"
        )
