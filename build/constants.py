"""Constants for image build."""

# As we are running the server with an unprivileged user, we need to use
# a high port.
APPLICATION_SERVER_PORT: str = "8000"

PLATFORMS: list[str] = ["linux/amd64", "linux/arm64/v8"]
