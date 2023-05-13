from typing import List

_truthy_values = ("True", "true", "1")
_falsy_values = ("False", "false", "0")
_allowed_bool_values = (*_truthy_values, *_falsy_values)


def validate_choices(value, choices):
    assert (
        value in choices
    ), "{value} is not in the predefined choices {choices}".format(
        value=value, choices=", ".join(choices)
    )


def csv(value: str) -> List[str]:
    return list(element.strip() for element in value.split(","))


def boolean(value: str) -> bool:
    assert value in _allowed_bool_values, "value of {v} is not a bool".format(v=value)
    return value in _truthy_values
