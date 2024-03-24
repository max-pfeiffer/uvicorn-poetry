"""Test fixtures for image publishing."""

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="package")
def cli_runner() -> CliRunner:
    """Fixture providing a Click CLI runner.

    :return:
    """
    runner = CliRunner()
    return runner
