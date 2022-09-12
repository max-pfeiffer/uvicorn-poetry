from build.constants import APPLICATION_SERVER_PORT

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
