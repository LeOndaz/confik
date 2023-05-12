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
    """An interface to confik.get(...)

    :param key: The key name to get from environment
    :param default: The value to return if the key was not found
    :param cast: A function to call on the value after it's found
    :param default_factory: A function to call with the key to return a value if the value was not found
    :param choices: A choices list to ensure that the value is in it
    :param raise_exception: Raise exceptions if the value was not found
    :return: str
    """
    return confik.get(key, default, cast, default_factory, choices, raise_exception)
