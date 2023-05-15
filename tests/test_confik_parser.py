from pathlib import Path

from confik import EnvConfikParser


def test_create_confik_parser_with_str_path():
    assert EnvConfikParser("."), "Can't create parser with path as string"


def test_create_confik_parser_with_path():
    assert EnvConfikParser(Path(".")), "Can't create parser with path as pathlib.Path"
