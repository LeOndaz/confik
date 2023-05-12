import contextlib
import os
from pathlib import Path


class MapConfigToMappingProxy:
    def get_mapping(self, path):
        """
        Should return a mapping from the path given
        :param path: str
        :return: Mapping
        """
        raise NotImplementedError


class EnvMappingProxy(MapConfigToMappingProxy):
    def get_mapping(self, path):
        mapping = {}

        with contextlib.suppress(FileNotFoundError):
            with open(path, "r") as f:
                for line in f.readlines():
                    entry = line.strip().split("=")

                    if len(entry) == 1:
                        entry.append("")

                    name, value = entry
                    mapping[name] = value.replace('"', "")

        return mapping

    def __init__(self, path=Path("."), *args, **kwargs):
        assert isinstance(path, (str, Path)), "unsupported path type {t}".format(
            t=type(path)
        )

        if isinstance(path, str):
            path = Path(path)

        if path.suffix != ".env":
            path = path / ".env"

        self.environ = {
            **os.environ,
            **self.get_mapping(path),
        }

    def get(self, key, default):
        return self.environ.get(key, default)
