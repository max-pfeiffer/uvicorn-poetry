UVICORN_POETRY_IMAGE_NAME = "pfeiffermax/uvicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.10-bullseye",
    "python3.9.10-slim-bullseye",
    "python3.10.2-bullseye",
    "python3.10.2-slim-bullseye",
]
BASE_IMAGES = {
    TARGET_ARCHITECTURES[0]: "python:3.9.10-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.10-slim-bullseye",
    TARGET_ARCHITECTURES[2]: "python:3.10.2-bullseye",
    TARGET_ARCHITECTURES[3]: "python:3.10.2-slim-bullseye",
}
