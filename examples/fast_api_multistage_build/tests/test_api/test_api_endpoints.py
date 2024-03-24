"""Tests for API endpoints."""

import random

from app.main import HELLO_WORLD, ITEMS
from requests import Response
from starlette import status


def test_root(test_client):
    """Test for root endpoint.

    :param test_client:
    :return:
    """
    response: Response = test_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == HELLO_WORLD


def test_items(test_client):
    """Test for items endpoint.

    :param test_client:
    :return:
    """
    key, value = random.choice(list(ITEMS.items()))

    response: Response = test_client.get(f"/items/{key}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == value
