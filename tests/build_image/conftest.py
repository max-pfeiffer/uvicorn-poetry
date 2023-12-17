from os import getenv

import pytest
from python_on_whales import Builder, DockerClient

from build.constants import PLATFORMS, APPLICATION_SERVER_PORT
from build.utils import (
    get_image_reference,
    get_context,
    get_python_poetry_image_reference,
)
from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME
from tests.registry_container import DockerRegistryContainer
from tests.utils import (
    get_fast_api_multistage_context,
    get_fast_api_multistage_image_reference,
    get_fast_api_multistage_with_json_logging_context,
    get_fast_api_multistage_with_json_logging_image_reference,
)


@pytest.fixture(scope="session")
def cache_settings(python_version: str, os_variant: str) -> tuple:
    github_ref_name: str = getenv("GITHUB_REF_NAME")
    cache_scope: str = f"{python_version}-{os_variant}"

    if github_ref_name:
        cache_to: str = (
            f"type=gha,mode=max,scope={github_ref_name}-{cache_scope}"
        )
        cache_from: str = f"type=gha,scope={github_ref_name}-{cache_scope}"
    else:
        cache_to = f"type=local,mode=max,dest=/tmp,scope={cache_scope}"
        cache_from = f"type=local,src=/tmp,scope={cache_scope}"

    return cache_to, cache_from


@pytest.fixture(scope="package")
def registry_container() -> DockerRegistryContainer:
    registry_container = DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000)
    registry_container.start()
    yield registry_container
    registry_container.stop()


@pytest.fixture(scope="package")
def base_image_reference(
    docker_client: DockerClient,
    pow_buildx_builder: Builder,
    image_version: str,
    registry_container: DockerRegistryContainer,
    python_version: str,
    os_variant: str,
    cache_settings: tuple,
) -> str:
    docker_client.login(
        server=registry_container.get_registry(),
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    image_reference: str = get_image_reference(
        registry_container.get_registry(),
        image_version,
        python_version,
        os_variant,
    )

    docker_client.buildx.build(
        context_path=get_context(),
        build_args={
            "BASE_IMAGE": get_python_poetry_image_reference(
                python_version, os_variant
            ),
            "APPLICATION_SERVER_PORT": APPLICATION_SERVER_PORT,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=pow_buildx_builder,
        cache_to=cache_settings[0],
        cache_from=cache_settings[1],
        push=True,
    )
    yield image_reference


@pytest.fixture(scope="package")
def fast_api_multistage_image_reference(
    docker_client: DockerClient,
    pow_buildx_builder: Builder,
    registry_container: DockerRegistryContainer,
    image_version: str,
    python_version: str,
    os_variant: str,
    cache_settings: tuple,
    base_image_reference: str,
) -> str:
    docker_client.login(
        server=registry_container.get_registry(),
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    image_reference: str = get_fast_api_multistage_image_reference(
        registry_container.get_registry(),
        image_version,
        python_version,
        os_variant,
    )

    docker_client.buildx.build(
        context_path=get_fast_api_multistage_context(),
        target="production-image",
        build_args={
            "BASE_IMAGE": base_image_reference,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=pow_buildx_builder,
        cache_to=cache_settings[0],
        cache_from=cache_settings[1],
        push=True,
    )
    yield image_reference


@pytest.fixture(scope="package")
def fast_api_multistage_with_json_logging_image_reference(
    docker_client: DockerClient,
    pow_buildx_builder: Builder,
    registry_container: DockerRegistryContainer,
    image_version: str,
    python_version: str,
    os_variant: str,
    cache_settings: tuple,
    base_image_reference: str,
) -> str:
    docker_client.login(
        server=registry_container.get_registry(),
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    image_reference: str = (
        get_fast_api_multistage_with_json_logging_image_reference(
            registry_container.get_registry(),
            image_version,
            python_version,
            os_variant,
        )
    )

    docker_client.buildx.build(
        context_path=get_fast_api_multistage_with_json_logging_context(),
        target="production-image",
        build_args={
            "BASE_IMAGE": base_image_reference,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=pow_buildx_builder,
        cache_to=cache_settings[0],
        cache_from=cache_settings[1],
        push=True,
    )
    yield image_reference
