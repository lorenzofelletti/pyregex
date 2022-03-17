import string


class Token:
    pass


class ElementToken(Token):
    def __init__(self, char: str):
        super().__init__()
        self.type = 'element'
        self.char = char


class WildcardToken(Token):
    def __init__(self, wildcard_ch: str):
        super().__init__()
        self.type = 'wildcard'
        self.wildcard_ch = wildcard_ch
        self.char = wildcard_ch


class SpaceToken(Token):
    def __init__(self, space_ch: str) -> None:
        super().__init__()
        self.type = 'space'
        self.space_char = space_ch
        self.char = string.whitespace


class Wildcard(WildcardToken):
    def __init__(self):
        super().__init__(wildcard_ch='.')


class StartToken(Token):
    def __init__(self, start_ch: str):
        super().__init__()
        self.type = 'start'
        self.start_ch = start_ch
        self.char = start_ch


class Start(StartToken):
    def __init__(self):
        super().__init__(start_ch='^')


class EndToken(Token):
    def __init__(self, end_ch: str):
        super().__init__()
        self.type = 'end'
        self.end_ch = end_ch
        self.char = end_ch


class End(EndToken):
    def __init__(self):
        super().__init__(end_ch='$')


class Escape(Token):
    def __init__(self):
        super().__init__()
        self.type = 'escape'
        self.escape_char = '\\'
        self.char = '\\'


class Comma(Token):
    def __init__(self):
        super().__init__()
        self.type = 'comma'
        self.char = ','


class Parenthesis(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'parenthesis'
        self.side = side


class LeftParenthesis(Parenthesis):
    def __init__(self):
        super().__init__(side='L')
        self.char = '('


class RightParenthesis(Parenthesis):
    def __init__(self):
        super().__init__(side='R')
        self.char = ')'


class CurlyBrace(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'curly'
        self.side = side


class LeftCurlyBrace(CurlyBrace):
    def __init__(self):
        super().__init__(side='L')
        self.char = '{'


class RightCurlyBrace(CurlyBrace):
    def __init__(self):
        super().__init__(side='R')
        self.char = '}'


class Bracket(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'bracket'
        self.side = side


class LeftBracket(Bracket):
    def __init__(self):
        super().__init__(side='L')
        self.char = '['


class RightBracket(Bracket):
    def __init__(self):
        super().__init__(side='R')
        self.char = ']'


class Quantifier(Token):
    def __init__(self, quantity: int, qtifier_char: str):
        super().__init__()
        self.type = 'qtifier'
        self.quantity = quantity
        self.qtifier_char = qtifier_char
        self.char = qtifier_char


class ZeroOrMore(Quantifier):
    def __init__(self, qtifier_char: str):
        super().__init__(quantity='zeroOrMore', qtifier_char=qtifier_char)


class OneOrMore(Quantifier):
    def __init__(self, qtifier_char: str):
        super().__init__(quantity='oneOrMore', qtifier_char=qtifier_char)


class ZeroOrOne(Quantifier):
    def __init__(self, qtifier_char: str):
        super().__init__(quantity='zeroOrOne', qtifier_char=qtifier_char)


class Asterisk(ZeroOrMore):
    def __init__(self):
        super().__init__(qtifier_char='*')


class Plus(OneOrMore):
    def __init__(self):
        super().__init__(qtifier_char='+')


class QuestionMark(ZeroOrOne):
    def __init__(self):
        super().__init__(qtifier_char='?')


class OrToken(Token):
    def __init__(self, or_ch: str):
        super().__init__()
        self.type = 'or'
        self.or_ch = or_ch
        self.char = or_ch


class VerticalBar(OrToken):
    def __init__(self):
        super().__init__(or_ch='|')


class NotToken(Token):
    def __init__(self, not_ch: str):
        super().__init__()
        self.type = 'not'
        self.not_ch = not_ch
        self.char = not_ch


class Circumflex(NotToken):
    def __init__(self):
        super().__init__(not_ch='^')


class Dash(Token):
    def __init__(self):
        super().__init__()
        self.type = 'dash'
        self.ch = '-'
        self.char = '-'
