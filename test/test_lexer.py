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
    tokens = lexer.scan('a\\a\\t\.')
    assert type(tokens[1]) is ElementToken and tokens[1].char == 'a'


def test_escaping_get_tab(lexer):
    tokens = lexer.scan('a\h\t')
    assert type(tokens[2]) is ElementToken and tokens[2].char == '\t'


def test_escaping_wildcard(lexer):
    tokens = lexer.scan('\.')
    assert type(tokens[0]) is ElementToken and tokens[0].char == '.'


def test_get_comma(lexer):
    tokens = lexer.scan('a{3,5}')
    assert type(tokens[3]) is Comma


def test_comma_is_element(lexer):
    tokens = lexer.scan('a,')
    assert type(tokens[1]) is ElementToken
