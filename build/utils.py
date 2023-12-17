from pathlib import Path


def get_context() -> Path:
    return Path(__file__).parent.resolve()


def get_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    reference: str = f"{registry}/pfeiffermax/uvicorn-poetry:{image_version}-python{python_version}-{os_variant}"
    return reference


def get_python_poetry_image_reference(
    python_version: str,
    os_variant: str,
) -> str:
    reference: str = f"pfeiffermax/python-poetry:1.8.0-poetry1.7.1-python{python_version}-{os_variant}"
    return reference
