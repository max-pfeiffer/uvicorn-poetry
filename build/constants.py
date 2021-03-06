UVICORN_POETRY_IMAGE_NAME: str = "pfeiffermax/uvicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME: str = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.13-bullseye",
    "python3.9.13-slim-bullseye",
    "python3.10.5-bullseye",
    "python3.10.5-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[0]: "python:3.9.13-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.13-slim-bullseye",
    TARGET_ARCHITECTURES[2]: "python:3.10.5-bullseye",
    TARGET_ARCHITECTURES[3]: "python:3.10.5-slim-bullseye",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.13",
    TARGET_ARCHITECTURES[1]: "3.9.13",
    TARGET_ARCHITECTURES[2]: "3.10.5",
    TARGET_ARCHITECTURES[3]: "3.10.5",
}
POETRY_VERSION: str = "1.1.14"
