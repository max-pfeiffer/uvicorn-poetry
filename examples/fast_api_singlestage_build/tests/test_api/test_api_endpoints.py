import random

from requests import Response
from starlette import status

from app.main import ITEMS, HELLO_WORLD


def test_root(test_client):
    response: Response = test_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == HELLO_WORLD


def test_items(test_client):
    key, value = random.choice(list(ITEMS.items()))

    response: Response = test_client.get(f"/items/{key}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == value
