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


def test_wildcard(reng):
    assert (True, 2) == reng.match('.*a', 'aa')


def test_backtracking(reng):
    assert (True, 4) == reng.match('a*a', 'aaaa')


def test_or(reng):
    assert (True, 1) == reng.match('a.*|b', 'b')


def test_or_no_match(reng):
    res, consumed = reng.match('a|b', 'c')
    assert res == False


def test_bt_no_match(reng):
    res, consumed = reng.match('a{5}a', 'aaaaa')
    assert res == False
