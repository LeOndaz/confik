import contextlib
import os
from pathlib import Path


class EnvMappingProxy:
    def __init__(self, path=Path("."), *args, **kwargs):
        assert isinstance(path, (str, Path)), "unsupported path type {t}".format(
            t=type(path)
        )

        environ = os.environ.copy()

        if isinstance(path, str):
            path = Path(path)

        if path.suffix != ".env":
            path = path / ".env"

        with contextlib.suppress(FileNotFoundError):
            with open(path, "r") as f:
                for line in f.readlines():
                    entry = line.strip().split("=")

                    if len(entry) == 1:
                        entry.append("")

                    name, value = entry
                    environ[name] = value.replace('"', "")

        self.environ = environ

    def get(self, key, default):
        return self.environ.get(key, default)
