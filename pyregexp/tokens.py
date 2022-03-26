import string
from typing import Literal


class Token:
    """ Token base class."""

    def __init__(self) -> None:
        self.char: str = ''
    pass


class ElementToken(Token):
    """ Token that are not associated to special meaning."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class WildcardToken(Token):
    """ Token of a wildcard."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class SpaceToken(Token):
    """ Token of a space."""

    def __init__(self, char: str) -> None:
        super().__init__()
        self.char: str = string.whitespace


class Wildcard(WildcardToken):
    """ Token using '.' as wildcard."""

    def __init__(self):
        super().__init__(char='.')


class StartToken(Token):
    """ Token of match start."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class Start(StartToken):
    """ Token using '^' to match start."""

    def __init__(self):
        super().__init__(char='^')


class EndToken(Token):
    """ Token of match end."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class End(EndToken):
    """ Token using '$' to match end."""

    def __init__(self):
        super().__init__(char='$')


class Escape(Token):
    """ Token of the escape character."""

    def __init__(self):
        super().__init__()
        self.char = '\\'


class Comma(Token):
    """ Token of a comma."""

    def __init__(self):
        super().__init__()
        self.char = ','


class Parenthesis(Token):
    """ Token of a parenthesis."""

    def __init__(self):
        super().__init__()


class LeftParenthesis(Parenthesis):
    """ Left parenthesis token."""

    def __init__(self):
        super().__init__()
        self.char = '('


class RightParenthesis(Parenthesis):
    """ Right parenthesis token."""

    def __init__(self):
        super().__init__()
        self.char = ')'


class CurlyBrace(Token):
    """ Curly brace token."""

    def __init__(self):
        super().__init__()


class LeftCurlyBrace(CurlyBrace):
    """ Left curly brace token."""

    def __init__(self):
        super().__init__()
        self.char = '{'


class RightCurlyBrace(CurlyBrace):
    """ Right curly brace token."""

    def __init__(self):
        super().__init__()
        self.char = '}'


class Bracket(Token):
    """ Brackets token."""

    def __init__(self):
        super().__init__()


class LeftBracket(Bracket):
    """ Left bracke token."""

    def __init__(self):
        super().__init__()
        self.char = '['


class RightBracket(Bracket):
    """ Right bracket token."""

    def __init__(self):
        super().__init__()
        self.char = ']'


class Quantifier(Token):
    """ Quantifier token."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class ZeroOrMore(Quantifier):
    """ Quantifier 'zero or more' token."""

    def __init__(self, char: str):
        super().__init__(char=char)


class OneOrMore(Quantifier):
    """ Quantifier 'one or more' token."""

    def __init__(self, char: str):
        super().__init__(char=char)


class ZeroOrOne(Quantifier):
    """ Quantifier 'zero or one' token."""

    def __init__(self, char: str):
        super().__init__(char=char)


class Asterisk(ZeroOrMore):
    """ Quantifier 'zero or more' token using character '*'."""

    def __init__(self):
        super().__init__(char='*')


class Plus(OneOrMore):
    """ Quantifier 'one or more' token using character '+'."""

    def __init__(self):
        super().__init__(char='+')


class QuestionMark(ZeroOrOne):
    """ Quantifier 'zero or one' token using character '?'."""

    def __init__(self):
        super().__init__(char='?')


class OrToken(Token):
    """ Token of the or."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class VerticalBar(OrToken):
    """ Token of the or using '|'."""

    def __init__(self):
        super().__init__(char='|')


class NotToken(Token):
    """ Token of the negation."""

    def __init__(self, char: str):
        super().__init__()
        self.char: str = char


class Circumflex(NotToken):
    """ Token of the negation using '^'."""

    def __init__(self):
        super().__init__(char='^')


class Dash(Token):
    """ Token of the dash '-'."""

    def __init__(self):
        super().__init__()
        self.char = '-'
