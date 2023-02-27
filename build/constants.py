UVICORN_POETRY_IMAGE_NAME: str = "pfeiffermax/uvicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME: str = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.16-bullseye",
    "python3.9.16-slim-bullseye",
    "python3.10.9-bullseye",
    "python3.10.9-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[
        0
    ]: "pfeiffermax/python-poetry:1.1.0-poetry1.3.2-python3.9.16-bullseye@sha256:3795ff170e143a5dfa960a81356e4cb3406ed6a7a3ccea0156c14e5cf4a67053",
    TARGET_ARCHITECTURES[
        1
    ]: "pfeiffermax/python-poetry:1.1.0-poetry1.3.2-python3.9.16-slim-bullseye@sha256:c6f545f175e7369017ae8d39e54497cb423ff8291d1a492b086dcd1a7439f9b0",
    TARGET_ARCHITECTURES[
        2
    ]: "pfeiffermax/python-poetry:1.1.0-poetry1.3.2-python3.10.9-bullseye@sha256:c269b0872f11fd198703e9dea301a4cb3dd1bbd7e054ab723d801dccc0b631cd",
    TARGET_ARCHITECTURES[
        3
    ]: "pfeiffermax/python-poetry:1.1.0-poetry1.3.2-python3.10.9-slim-bullseye@sha256:ee99ee20733201523728147ab0c9117d22266994a1919ec0d64937133a51f07d",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.16",
    TARGET_ARCHITECTURES[1]: "3.9.16",
    TARGET_ARCHITECTURES[2]: "3.10.9",
    TARGET_ARCHITECTURES[3]: "3.10.9",
}

# As we are running the server with an unprivileged user, we need to use
# a high port.
APPLICATION_SERVER_PORT: str = "8000"
