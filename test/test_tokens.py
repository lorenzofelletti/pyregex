import pytest
from ..src.tokens import Asterisk, Bracket, Circumflex, Comma, CurlyBrace, Dash, ElementToken, End, EndToken, Escape, LeftBracket, LeftCurlyBrace, LeftParenthesis, NotToken, OneOrMore, OrToken, Parenthesis, Plus, Quantifier, QuestionMark, RightBracket, RightCurlyBrace, RightParenthesis, SpaceToken, Start, StartToken, Token, VerticalBar, Wildcard, WildcardToken, ZeroOrMore, ZeroOrOne


def test_Asterisk():
    assert issubclass(Asterisk, ZeroOrMore)

    a = Asterisk()
    assert a is not None

    assert a.type == 'qtifier'


def test_NotToken():
    assert issubclass(NotToken, Token) == True

    nt = NotToken(not_ch='^')
    assert nt is not None

    assert nt.type == 'not'
    assert nt.not_ch == '^'
    assert nt.char == nt.not_ch
