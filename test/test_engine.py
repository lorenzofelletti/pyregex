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
    res, consumed = reng.match('^a|b$', 'c')
    assert res == False


def test_or_no_match_with_bt(reng):
    res, consumed = reng.match('a|b', 'c')
    assert res == False


def test_bt_no_match(reng):
    res, consumed = reng.match('a{5}a', 'aaaaa')
    assert res == False


def test_match_group_zero_or_more(reng):
    res, consumed = reng.match('(a)*', 'aa')
    assert (True, 2) == (res, consumed)


def test_fail_group_one_or_more(reng):
    res, cons = reng.match('^(a)+', 'b')
    assert res == False


def test_complex_match(reng):
    res, cons = reng.match('^(a|b+c)?[n-z]{2}', 'axx')
    assert res == True


def test_complex_match_2(reng):
    res, cons = reng.match('^(a|b+c)?[n-z]{2}', 'xx')
    assert res == True


def test_match_mail_simple(reng):
    res, cons = reng.match('.*@.*\.(com|it)', 'vr@gmail.com')
    assert res == True


def test_bt_index_leaf(reng):
    res, cons = reng.match('^aaaa.*a$', 'aaaaa')
    assert res == True


def test_bt_index_or(reng):
    res, cons = reng.match('^x(a|b)?bc$', 'xbc')
    assert res == True


def test_bt_index_group(reng):
    res, cons = reng.match('^x(a)?ac$', 'xac')
    assert res == True


def test_match_or_left(reng):
    res, cons = reng.match('na|nb', 'na')
    assert res == True


def test_match_or_right(reng):
    res, cons = reng.match('na|nb', 'nb')
    assert res == True


def test_match_or_right_at_start_end(reng):
    res, cons = reng.match('^na|nb$', 'nb')
    assert res == True
