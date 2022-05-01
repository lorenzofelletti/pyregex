import pytest
from ..pyregexp.engine import RegexEngine


@pytest.fixture
def reng() -> RegexEngine:
    return RegexEngine()


def test_1(reng: RegexEngine):
    regex = r"(ad+a)*a"
    test_str = "adaa"

    res, consumed, matches = reng.match(regex, test_str, True, True)

    assert res == True
    consumed == len(test_str)
    assert len(matches) == 1


def test_2(reng: RegexEngine):
    regex = r"0|1|2|3"
    test_str = "3210"

    res, consumed, matches = reng.match(regex, test_str, True, True)

    assert res == True
    consumed == len(test_str)
    assert len(matches) == 4
