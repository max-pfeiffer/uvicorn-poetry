import click
from build.constants import PLATFORMS, APPLICATION_SERVER_PORT
from build.utils import get_context, get_image_reference
from pathlib import Path
from python_on_whales import DockerClient, Builder
from os import getenv


@click.command()
@click.option(
    "--docker-hub-username",
    envvar="DOCKER_HUB_USERNAME",
    help="Docker Hub username",
)
@click.option(
    "--docker-hub-password",
    envvar="DOCKER_HUB_PASSWORD",
    help="Docker Hub password",
)
@click.option(
    "--version-tag", envvar="GIT_TAG_NAME", required=True, help="Version tag"
)
@click.option(
    "--python-version",
    envvar="PYTHON_VERSION",
    required=True,
    help="Python version",
)
@click.option(
    "--os-variant",
    envvar="OS_VARIANT",
    required=True,
    help="Operating system variant",
)
@click.option("--registry", envvar="REGISTRY", help="Docker registry")
def main(
    docker_hub_username: str,
    docker_hub_password: str,
    version_tag: str,
    python_version: str,
    os_variant: str,
    registry: str,
) -> None:
    github_ref_name: str = getenv("GITHUB_REF_NAME")
    context: Path = get_context()
    image_reference: str = get_image_reference(
        registry, version_tag, python_version, os_variant
    )
    cache_scope: str = f"{python_version}-{os_variant}"

    if github_ref_name:
        cache_to: str = (
            f"type=gha,mode=max,scope={github_ref_name}-{cache_scope}"
        )
        cache_from: str = f"type=gha,scope={github_ref_name}-{cache_scope}"
    else:
        cache_to = f"type=local,mode=max,dest=/tmp,scope={cache_scope}"
        cache_from = f"type=local,src=/tmp,scope={cache_scope}"

    docker_client: DockerClient = DockerClient()
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )

    docker_client.login(
        server=registry,
        username=docker_hub_username,
        password=docker_hub_password,
    )

    docker_client.buildx.build(
        context_path=context,
        build_args={
            "BASE_IMAGE": f"pfeiffermax/python-poetry:1.8.0-poetry1.7.1-python{python_version}-{os_variant}",
            "APPLICATION_SERVER_PORT": APPLICATION_SERVER_PORT,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=builder,
        cache_to=cache_to,
        cache_from=cache_from,
        push=True,
    )

    # Cleanup
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
