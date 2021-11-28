UVICORN_GUNICORN_POETRY_IMAGE_NAME = "pfeiffermax/uvicorn-gunicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.8-bullseye",
    "python3.9.8-slim-bullseye",
]
BASE_IMAGES = {
    TARGET_ARCHITECTURES[0]: "python:3.9.8-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.8-slim-bullseye",
}
