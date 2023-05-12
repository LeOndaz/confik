from pathlib import Path

from confik import ConfikParser


def test_create_confik_parser_with_str_path():
    assert ConfikParser("."), "Can't create parser with path as string"


def test_create_confik_parser_with_path():
    assert ConfikParser(Path(".")), "Can't create parser with path as pathlib.Path"
