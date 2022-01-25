import pytest
from ..src.tokens import *
from ..src.lexer import Lexer


@pytest.fixture
def lexer():
    return Lexer()


def test_simple_re_lexing(lexer):
    tokens = lexer.scan('a')
    assert tokens[0].char == 'a'


def test_escaping_char(lexer):
    tokens = lexer.scan(r'a\\a\\t\.')
    assert type(tokens[1]) is ElementToken and tokens[1].char == '\\'


def test_escaping_get_tab(lexer):
    tokens = lexer.scan(r'a\h\t')
    assert type(tokens[2]) is ElementToken and tokens[2].char == '\t'


def test_escaping_wildcard(lexer):
    tokens = lexer.scan(r'\.')
    assert type(tokens[0]) is ElementToken and tokens[0].char == '.'


def test_get_comma(lexer):
    tokens = lexer.scan('a{3,5}')
    assert type(tokens[3]) is Comma


def test_comma_is_element(lexer):
    tokens = lexer.scan('a,')
    assert type(tokens[1]) is ElementToken


def test_match_start(lexer):
    tokens = lexer.scan('^a')
    assert type(tokens[0]) is Start


def test_match_end(lexer):
    tokens = lexer.scan(r'fdsad\$cs$')
    assert type(tokens[len(tokens) - 1]) is End


def test_fail_curly(lexer):
    with pytest.raises(Exception):
        lexer.scan('advfe{a}')


def test_lexer_1(lexer):
    tokens = lexer.scan(r'-\\\/\s~')
    assert len(tokens) == 5
    assert type(tokens[0]) is Dash
    assert type(tokens[1]) is ElementToken
    assert type(tokens[2]) is ElementToken
    assert type(tokens[3]) is SpaceToken
    assert type(tokens[4]) is ElementToken
