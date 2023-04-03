from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import bcrypt
from testcontainers.core.container import DockerContainer


# https://docs.docker.com/registry/
class DockerRegistryContainer(DockerContainer):
    def __init__(
        self,
        image="registry:latest",
        port: int = 5000,
        username: str = None,
        password: str = None,
    ) -> None:
        super().__init__(image=image)
        self.port_to_expose = port
        self.with_bind_ports(5000, port)
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.htpasswd_file: Optional[Path] = None

    def start(self):
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

    def stop(self, force=True, delete_volume=True):
        super().stop(force=force, delete_volume=delete_volume)
        # Remove the password file
        if self.htpasswd_file:
            self.htpasswd_file.unlink()

    def get_registry(self) -> str:
        return f"localhost:{self.port_to_expose}"
