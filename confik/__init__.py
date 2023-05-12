from .exceptions import ConfikError
from .parsers import ConfikParser
from .utils import csv

confik = ConfikParser()


def get(
    key,
    default=None,
    cast=None,
    default_factory=None,
    choices=tuple(),
    raise_exception=False,
):
    return confik.get(key, default, cast, default_factory, choices, raise_exception)
