import string
from typing import Literal


class Token:
    """ Tokens base class."""

    def __init__(self) -> None:
        self.type: str = ''
        self.char: str = ''
    pass


class ElementToken(Token):
    """ Token that are not associated to special meaning."""

    def __init__(self, char: str):
        super().__init__()
        self.type = 'element'
        self.char: str = char


class WildcardToken(Token):
    """ Token of a wildcard."""

    def __init__(self, wildcard_ch: str):
        super().__init__()
        self.type = 'wildcard'
        self.wildcard_ch: str = wildcard_ch
        self.char: str = wildcard_ch


class SpaceToken(Token):
    """ Token of a space."""

    def __init__(self, space_ch: str) -> None:
        super().__init__()
        self.type = 'space'
        self.space_char: str = space_ch
        self.char: str = string.whitespace


class Wildcard(WildcardToken):
    """ Token using '.' as wildcard."""

    def __init__(self):
        super().__init__(wildcard_ch='.')


class StartToken(Token):
    """ Token of match start."""

    def __init__(self, start_ch: str):
        super().__init__()
        self.type = 'start'
        self.start_ch: str = start_ch
        self.char: str = start_ch


class Start(StartToken):
    """ Token using '^' to match start."""

    def __init__(self):
        super().__init__(start_ch='^')


class EndToken(Token):
    """ Token of match end."""

    def __init__(self, end_ch: str):
        super().__init__()
        self.type = 'end'
        self.end_ch: str = end_ch
        self.char: str = end_ch


class End(EndToken):
    """ Token using '$' to match end."""

    def __init__(self):
        super().__init__(end_ch='$')


class Escape(Token):
    """ Token of the escape character."""

    def __init__(self):
        super().__init__()
        self.type = 'escape'
        self.escape_char = '\\'
        self.char = '\\'


class Comma(Token):
    """ Token of a comma."""

    def __init__(self):
        super().__init__()
        self.type = 'comma'
        self.char = ','


class Parenthesis(Token):
    """ Token of a parenthesis."""

    def __init__(self, side: str):
        super().__init__()
        self.type = 'parenthesis'
        self.side: Literal["L", "R"] = side


class LeftParenthesis(Parenthesis):
    """ Left parenthesis token."""

    def __init__(self):
        super().__init__(side='L')
        self.char = '('


class RightParenthesis(Parenthesis):
    """ Right parenthesis token."""

    def __init__(self):
        super().__init__(side='R')
        self.char = ')'


class CurlyBrace(Token):
    """ Curly brace token."""

    def __init__(self, side: str):
        super().__init__()
        self.type = 'curly'
        self.side: Literal["L", "R"] = side


class LeftCurlyBrace(CurlyBrace):
    """ Left curly brace token."""

    def __init__(self):
        super().__init__(side='L')
        self.char = '{'


class RightCurlyBrace(CurlyBrace):
    """ Right curly brace token."""

    def __init__(self):
        super().__init__(side='R')
        self.char = '}'


class Bracket(Token):
    """ Brackets token."""

    def __init__(self, side: str):
        super().__init__()
        self.type = 'bracket'
        self.side: Literal["L", "R"] = side


class LeftBracket(Bracket):
    """ Left bracke token."""

    def __init__(self):
        super().__init__(side='L')
        self.char = '['


class RightBracket(Bracket):
    """ Right bracket token."""

    def __init__(self):
        super().__init__(side='R')
        self.char = ']'


class Quantifier(Token):
    """ Quantifier token."""

    def __init__(self, quantity: str, qtifier_char: str):
        super().__init__()
        self.type = 'qtifier'
        self.quantity: str = quantity
        self.qtifier_char: str = qtifier_char
        self.char: str = qtifier_char


class ZeroOrMore(Quantifier):
    """ Quantifier 'zero or more' token."""

    def __init__(self, qtifier_char: str):
        super().__init__(quantity='zeroOrMore', qtifier_char=qtifier_char)


class OneOrMore(Quantifier):
    """ Quantifier 'one or more' token."""

    def __init__(self, qtifier_char: str):
        super().__init__(quantity='oneOrMore', qtifier_char=qtifier_char)


class ZeroOrOne(Quantifier):
    """ Quantifier 'zero or one' token."""

    def __init__(self, qtifier_char: str):
        super().__init__(quantity='zeroOrOne', qtifier_char=qtifier_char)


class Asterisk(ZeroOrMore):
    """ Quantifier 'zero or more' token using character '*'."""

    def __init__(self):
        super().__init__(qtifier_char='*')


class Plus(OneOrMore):
    """ Quantifier 'one or more' token using character '+'."""

    def __init__(self):
        super().__init__(qtifier_char='+')


class QuestionMark(ZeroOrOne):
    """ Quantifier 'zero or one' token using character '?'."""

    def __init__(self):
        super().__init__(qtifier_char='?')


class OrToken(Token):
    """ Token of the or."""

    def __init__(self, or_ch: str):
        super().__init__()
        self.type = 'or'
        self.or_ch: str = or_ch
        self.char: str = or_ch


class VerticalBar(OrToken):
    """ Token of the or using '|'."""

    def __init__(self):
        super().__init__(or_ch='|')


class NotToken(Token):
    """ Token of the negation."""

    def __init__(self, not_ch: str):
        super().__init__()
        self.type = 'not'
        self.not_ch: str = not_ch
        self.char: str = not_ch


class Circumflex(NotToken):
    """ Token of the negation using '^'."""

    def __init__(self):
        super().__init__(not_ch='^')


class Dash(Token):
    """ Token of the dash '-'."""

    def __init__(self):
        super().__init__()
        self.type = 'dash'
        self.ch = '-'
        self.char = '-'
