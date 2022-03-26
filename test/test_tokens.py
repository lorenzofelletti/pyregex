from ..pyregexp.tokens import Asterisk, Bracket, Circumflex, Comma, CurlyBrace, Dash, ElementToken, End, EndToken, Escape, LeftBracket, LeftCurlyBrace, LeftParenthesis, NotToken, OneOrMore, OrToken, Parenthesis, Plus, Quantifier, QuestionMark, RightBracket, RightCurlyBrace, RightParenthesis, SpaceToken, Start, StartToken, Token, VerticalBar, Wildcard, WildcardToken, ZeroOrMore, ZeroOrOne


def test_Asterisk():
    assert issubclass(Asterisk, ZeroOrMore)

    a = Asterisk()
    assert a is not None

    assert type(a) == Asterisk


def test_NotToken():
    assert issubclass(NotToken, Token) == True

    nt = NotToken(char='^')
    assert nt is not None
    assert nt.char == '^'


def test_Bracket():
    br = Bracket()
    assert br is not None
    br = LeftBracket()
    assert br is not None
    br = RightBracket()
    assert br is not None


def test_Escape():
    escape = Escape()
    assert escape is not None
