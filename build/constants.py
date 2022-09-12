UVICORN_POETRY_IMAGE_NAME: str = "pfeiffermax/uvicorn-poetry"
FAST_API_SINGLESTAGE_IMAGE_NAME: str = "fast-api-singlestage-build"
FAST_API_MULTISTAGE_IMAGE_NAME: str = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.14-bullseye",
    "python3.9.14-slim-bullseye",
    "python3.10.7-bullseye",
    "python3.10.7-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[0]: "python:3.9.14-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.14-slim-bullseye",
    TARGET_ARCHITECTURES[2]: "python:3.10.7-bullseye",
    TARGET_ARCHITECTURES[3]: "python:3.10.7-slim-bullseye",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.14",
    TARGET_ARCHITECTURES[1]: "3.9.14",
    TARGET_ARCHITECTURES[2]: "3.10.7",
    TARGET_ARCHITECTURES[3]: "3.10.7",
}
POETRY_VERSION: str = "1.2.0"
APPLICATION_SERVER_PORT: str = "80"
