import os

import docker
from dotenv import load_dotenv

from build.constants import (
    TARGET_ARCHITECTURES,
    UVICORN_GUNICORN_POETRY_IMAGE_NAME,
)
from build.images import UvicornGunicornPoetryImage

environment_variables_loaded: bool = load_dotenv()

docker_hub_username: str = os.getenv("DOCKER_HUB_USERNAME")
docker_hub_password: str = os.getenv("DOCKER_HUB_PASSWORD")
version_tag: str = os.getenv("GIT_TAG_NAME")


def main() -> None:
    docker_client: docker.client = docker.from_env()

    for target_architecture in TARGET_ARCHITECTURES:
        new_uvicorn_gunicorn_poetry_image: UvicornGunicornPoetryImage = (
            UvicornGunicornPoetryImage(docker_client)
        )

        # Delete old existing images
        for old_image in docker_client.images.list(
            new_uvicorn_gunicorn_poetry_image.image_name
        ):
            for tag in old_image.tags:
                docker_client.images.remove(tag, force=True)

        new_uvicorn_gunicorn_poetry_image.build(
            target_architecture, version=version_tag
        )

        # https://docs.docker.com/engine/reference/commandline/push/
        # https://docs.docker.com/engine/reference/commandline/tag/
        # https://docs.docker.com/engine/reference/commandline/image_tag/
        docker_client.login(
            username=docker_hub_username, password=docker_hub_password
        )
        for line in docker_client.images.push(
            UVICORN_GUNICORN_POETRY_IMAGE_NAME,
            tag=new_uvicorn_gunicorn_poetry_image.image_tag,
            stream=True,
            decode=True,
        ):
            print(line)
    docker_client.close()


if __name__ == "__main__":
    main()
