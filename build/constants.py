UVICORN_POETRY_IMAGE_NAME = "pfeiffermax/uvicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.11-bullseye",
    "python3.9.11-slim-bullseye",
    "python3.10.3-bullseye",
    "python3.10.3-slim-bullseye",
]
BASE_IMAGES = {
    TARGET_ARCHITECTURES[0]: "python:3.9.11-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.11-slim-bullseye",
    TARGET_ARCHITECTURES[2]: "python:3.10.3-bullseye",
    TARGET_ARCHITECTURES[3]: "python:3.10.3-slim-bullseye",
}
PYTHON_VERSIONS = {
    TARGET_ARCHITECTURES[0]: "3.9.11",
    TARGET_ARCHITECTURES[1]: "3.9.11",
    TARGET_ARCHITECTURES[2]: "3.10.3",
    TARGET_ARCHITECTURES[3]: "3.10.3",
}
