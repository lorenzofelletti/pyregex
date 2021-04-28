import pytest
from ..src.engine import RegexEngine


@pytest.fixture
def reng():
    return RegexEngine()


def test_simplest(reng):
    assert (True, 1) == reng.match('a', 'a')


def test_simplest_with_wildcard(reng):
    assert (True, 1) == reng.match('.', 'a')


def test_simplest_but_longer(reng):
    assert (True, 3) == reng.match('a.c', 'abc')
