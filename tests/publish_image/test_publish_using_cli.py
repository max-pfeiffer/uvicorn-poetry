from click.testing import CliRunner, Result
from docker.errors import APIError

from build.publish import main
from tests.registry_container import DockerRegistryContainer


def test_missing_options_and_env(cli_runner: CliRunner):
    result: Result = cli_runner.invoke(main)
    assert result.exit_code == 2


def test_wrong_credentials_in_options(cli_runner: CliRunner):
    result: Result = cli_runner.invoke(
        main,
        args=[
            "--docker-hub-username",
            "foo",
            "--docker-hub-password",
            "bar",
            "--version-tag",
            "1.0.0",
        ],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, APIError)


def test_wrong_credentials_in_env(cli_runner: CliRunner):
    result: Result = cli_runner.invoke(
        main,
        env={
            "DOCKER_HUB_USERNAME": "foo",
            "DOCKER_HUB_PASSWORD": "bar",
            "GIT_TAG_NAME": "1.0.0",
        },
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, APIError)


def test_registry_without_credentials(cli_runner):
    with DockerRegistryContainer() as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--version-tag",
                "1.0.0",
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 0


def test_registry_with_credentials(cli_runner):
    username: str = "foo"
    password: str = "bar"

    with DockerRegistryContainer(
        username=username, password=password
    ) as docker_registry:
        result: Result = cli_runner.invoke(
            main,
            args=[
                "--docker-hub-username",
                username,
                "--docker-hub-password",
                password,
                "--version-tag",
                "1.0.0",
                "--registry",
                docker_registry.get_registry(),
            ],
        )
        assert result.exit_code == 0
