TARGET_ARCHITECTURES: list[str] = [
    "python3.9.16-bullseye",
    "python3.9.16-slim-bullseye",
    "python3.10.10-bullseye",
    "python3.10.10-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[
        0
    ]: "pfeiffermax/python-poetry:1.2.0-poetry1.4.1-python3.9.16-bullseye@sha256:54037cfdca026b17e7a57664dff47bf04e7849074d3ab62271ecad0446ef0322",
    TARGET_ARCHITECTURES[
        1
    ]: "pfeiffermax/python-poetry:1.2.0-poetry1.4.1-python3.9.16-slim-bullseye@sha256:c0b8d9c28c5717074c481dfdf1d8bd3aaa0b83a5e2a9e37c77be7af19d70d0ce",
    TARGET_ARCHITECTURES[
        2
    ]: "pfeiffermax/python-poetry:1.2.0-poetry1.4.1-python3.10.10-bullseye@sha256:5a81c8c86132e504db2b7329f5e41cd32bddebf811d83a0d356edbca0d81135c",
    TARGET_ARCHITECTURES[
        3
    ]: "pfeiffermax/python-poetry:1.2.0-poetry1.4.1-python3.10.10-slim-bullseye@sha256:289c6beb568991811629c91cdcb3841ceb95bf0a017c3e411f4b71e18043ef15",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.16",
    TARGET_ARCHITECTURES[1]: "3.9.16",
    TARGET_ARCHITECTURES[2]: "3.10.10",
    TARGET_ARCHITECTURES[3]: "3.10.10",
}

# As we are running the server with an unprivileged user, we need to use
# a high port.
APPLICATION_SERVER_PORT: str = "8000"
