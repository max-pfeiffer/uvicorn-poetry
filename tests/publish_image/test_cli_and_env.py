"""Tests for using CLI aptions and environment variables."""

from click.testing import CliRunner, Result

from build.publish import main


def test_missing_options_and_env(cli_runner: CliRunner) -> None:
    """Test if image publishing fails without providing anything.

    :param cli_runner:
    :return:
    """
    result: Result = cli_runner.invoke(main)
    assert result.exit_code == 2
