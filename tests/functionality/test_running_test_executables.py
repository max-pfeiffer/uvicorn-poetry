from uuid import uuid4

import pytest


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_running_black_test_image(
    docker_client,
    fast_api_multistage_development_black_test_image,
    cleaned_up_test_container,
) -> None:
    api_response: dict = docker_client.containers.run(
        fast_api_multistage_development_black_test_image,
        name=cleaned_up_test_container,
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_running_unit_test_image(
    docker_client,
    fast_api_multistage_development_unit_test_image,
    cleaned_up_test_container,
) -> None:
    api_response: dict = docker_client.containers.run(
        fast_api_multistage_development_unit_test_image,
        name=cleaned_up_test_container,
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0
