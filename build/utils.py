"""Utilities for image publishing."""

from pathlib import Path


def get_context() -> Path:
    """Return Docker build context.

    :return:
    """
    return Path(__file__).parent.resolve()


def get_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/pfeiffermax/uvicorn-poetry:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference


def get_python_poetry_image_reference(
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for base image.

    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"pfeiffermax/python-poetry:1.8.0-poetry1.7.1-python"
        f"{python_version}-{os_variant}"
    )
    return reference
