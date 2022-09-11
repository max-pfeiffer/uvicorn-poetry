from tests.constants import TEST_CONTAINER_NAME


def test_running_black_test_image(
    docker_client, fast_api_multistage_development_black_test_image
) -> None:
    api_response: dict = docker_client.containers.run(
        fast_api_multistage_development_black_test_image,
        name=TEST_CONTAINER_NAME,
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0


def test_running_unit_test_image(
    docker_client, fast_api_multistage_development_unit_test_image
) -> None:
    api_response: dict = docker_client.containers.run(
        fast_api_multistage_development_unit_test_image,
        name=TEST_CONTAINER_NAME,
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0
