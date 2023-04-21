import pytest
from click.testing import CliRunner, Result

from build.publish import main


@pytest.mark.usefixtures("cleanup_images")
def test_missing_options_and_env(cli_runner: CliRunner):
    result: Result = cli_runner.invoke(main)
    assert result.exit_code == 2
