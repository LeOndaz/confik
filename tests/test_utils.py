import pytest

from confik.utils import validate_choices


def test_validate_choices():
    choices = ["LeOndaz", "Ahmed"]
    validate_choices("LeOndaz", choices)
