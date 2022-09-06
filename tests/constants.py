from build.constants import APPLICATION_SERVER_PORT

TEST_CONTAINER_NAME: str = "uvicorn-poetry-test"
SLEEP_TIME: float = 3.0
HELLO_WORLD: str = "Hello World!"
DEFAULT_UVICORN_CONFIG: dict[str, str] = {
    "workers": "1",
    "host": "0.0.0.0",
    "port": APPLICATION_SERVER_PORT,
}
DEVELOPMENT_UVICORN_CONFIG: dict[str, str] = {
    "workers": "1",
    "host": "0.0.0.0",
    "port": APPLICATION_SERVER_PORT,
}
JSON_LOGGING_CONFIG: dict[str, str] = {
    "workers": "1",
    "host": "0.0.0.0",
    "port": APPLICATION_SERVER_PORT,
}
VERSIONS: list[str] = ["1.0.0", "3.74.4", "21.4.10"]
