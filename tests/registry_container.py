from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import bcrypt
from testcontainers.core.container import DockerContainer


# https://docs.docker.com/registry/
class DockerRegistryContainer(DockerContainer):
    def __init__(
        self,
        image: str = "registry:latest",
        port: int = 5000,
        username: str = None,
        password: str = None,
        **kwargs,
    ) -> None:
        super().__init__(image=image, **kwargs)
        self.port_to_expose = port
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.htpasswd_file: Optional[Path] = None
        self.with_exposed_ports(self.port_to_expose)

    def start(self):
        # Create the password file
        if self.username and self.password:
            hashed_password: str = bcrypt.hashpw(
                self.password.encode("utf-8"),
                bcrypt.gensalt(rounds=12, prefix=b"2a"),
            ).decode("utf-8")
            content = f"{self.username}:{hashed_password}"

            with NamedTemporaryFile(delete=False) as file:
                file.write(content.encode("utf-8"))
                self.htpasswd_file = Path(file.name)

                host_dir: str = str(self.htpasswd_file.parent.resolve())
                tmp_file: str = self.htpasswd_file.name

                self.with_volume_mapping(host_dir, "/htpasswd")
                self.with_env("REGISTRY_AUTH_HTPASSWD_REALM", "local-registry")
                self.with_env(
                    "REGISTRY_AUTH_HTPASSWD_PATH", f"/htpasswd/{tmp_file}"
                )

        super().start()
        return self

    def stop(self, **kwargs):
        super().stop(**kwargs)
        # Remove the password file
        if self.htpasswd_file:
            self.htpasswd_file.unlink()

    def get_registry(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.port_to_expose)
        return f"{host}:{port}"
