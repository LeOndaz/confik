import contextlib
import os
from pathlib import Path
from typing import Union


class MapConfiKToMappingProxy:
    async def aget(self, key, default=None):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def get_mapping(self, path):
        """
        Should return a mapping from the path given
        :param path: str
        :return: Mapping
        """
        return NotImplementedError


class EnvMappingProxy(MapConfiKToMappingProxy):
    def __init__(self, path: Union[Path, str] = Path("."), *args, **kwargs):
        assert isinstance(path, (str, Path)), "unsupported path type {t}".format(
            t=type(path)
        )

        if isinstance(path, str):
            path = Path(path)

        if path.suffix != ".env":
            path = path / ".env"

        self.environ = self.get_mapping(path)

    def get(self, key, default=None):
        return self.environ.get(key, default)

    def get_mapping(self, path):
        mapping = os.environ.copy()

        with contextlib.suppress(FileNotFoundError):
            with open(path, "r") as f:
                for line in f.readlines():
                    entry = line.strip().split("=", 1)

                    if len(entry) == 1:
                        entry.append("")

                    name, value = entry
                    mapping[name] = value.replace('"', "").replace("'", "")

        return mapping
