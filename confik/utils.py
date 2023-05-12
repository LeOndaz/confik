def validate_choices(value, choices):
    assert (
        value in choices
    ), "{value} is not in the predefined choices {choices}".format(
        value=value, choices=", ".join(choices)
    )


def csv(value: str):
    return list(element.strip() for element in value.split(","))
