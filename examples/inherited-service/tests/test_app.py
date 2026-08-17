from src.app import parse, active_only


def test_parse_splits_on_comma():
    assert parse("a,b,active") == ["a", "b", "active"]


def test_active_only_filters():
    assert active_only([["a", "active"], ["b", "retired"]]) == [["a", "active"]]
