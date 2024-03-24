"""Main module."""

from typing import Dict

from fastapi import FastAPI

app = FastAPI()

HELLO_WORLD: str = "Hello World!"
ITEMS: Dict[str, str] = {"1": "sausage", "2": "ham", "3": "tofu"}


@app.get("/")
def read_root():
    """Root endpoint.

    :return:
    """
    return HELLO_WORLD


@app.get("/items/{item_id}")
def read_item(item_id: str):
    """Items endpoint.

    :param item_id:
    :return:
    """
    return ITEMS[item_id]


def get_app():
    """Return application.

    :return:
    """
    return app
