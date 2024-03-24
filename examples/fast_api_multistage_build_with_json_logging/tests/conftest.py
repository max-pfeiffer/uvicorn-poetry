"""Fixtures for tests."""

import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture for providing a test client.

    :return:
    """
    return TestClient(app)
