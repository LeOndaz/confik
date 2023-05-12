import random
import string

import pytest

import confik
from confik import ConfikError


def get_random_key():
    return "".join(random.choice(string.ascii_uppercase) for _ in range(20))


def test_read_variable_from_env():
    env = confik.get("VARIABLE")
    assert env == "VALUE", "VARIABLE is equal to {v}".format(v=env)


def test_read_variable_from_os():
    env = confik.get("PATH")
    assert env, "env is {v}".format(v=env)


def test_get_non_existent_key():
    random_key = get_random_key()

    with pytest.raises(ConfikError):
        confik.get(random_key)


def test_default_value():
    random_key = get_random_key()

    env = confik.get(random_key, "DEFAULT_VALUE")
    assert (
        env == "DEFAULT_VALUE"
    ), "env is not equal to default value, current value is {v}".format(v=env)


def test_default_factory():
    random_key = get_random_key()
    env = confik.get(random_key, default_factory=lambda x: "DEFAULT_FACTORY_VALUE")

    assert env == "DEFAULT_FACTORY_VALUE"


def test_cast_to_csv():
    env = confik.get("VARIABLE_WITH_MULTI_VALUES", cast=confik.csv)
    assert len(env) == 4
    assert env == ["V1", "V2", "V3", "V4"]


def test_csv_elements_has_no_trailing_or_preceding_space():
    env = confik.get("VARIABLE_WITH_MULTI_VALUES", cast=confik.csv)

    for i, element in enumerate(env):
        assert bool(
            element.find(" ")
        ), "element at index {i} has space {element}".format(
            i=i,
            element=element,
        )


def test_read_truthy_bools():
    for i in range(1, 4):
        env = confik.get("VARIABLE_WITH_TRUE_VALUE_{i}".format(i=i), cast=bool)
        assert env is True, "Expected True, got {}".format(env)


def test_read_falsy_bools():
    for i in range(1, 4):
        env = confik.get("VARIABLE_WITH_FALSE_VALUE_{i}".format(i=i), cast=bool)
        assert env is False, "Expected False, got {}".format(env)


def test_read_integer():
    env = confik.get("VARIABLE_WITH_INTEGER", cast=int)
    assert isinstance(env, int)
