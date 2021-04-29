class Token:
    pass


class ElementToken(Token):
    def __init__(self, char):
        super().__init__()
        self.type = 'element'
        self.char = char


class WildcardToken(Token):
    def __init__(self, wildcard_ch):
        super().__init__()
        self.type = 'wildcard'
        self.wildcard_ch = wildcard_ch


class Wildcard(WildcardToken):
    def __init__(self):
        super().__init__(wildcard_ch='.')


class StartToken(Token):
    def __init__(self, start_ch):
        super().__init__()
        self.type = 'start'
        self.start_ch = start_ch


class Start(StartToken):
    def __init__(self):
        super().__init__(start_ch='^')


class EndToken(Token):
    def __init__(self, end_ch):
        super().__init__()
        self.type = 'end'
        self.end_ch = end_ch


class End(EndToken):
    def __init__(self):
        super().__init__(end_ch='$')


class Escape(Token):
    def __init__(self):
        super().__init__()
        self.type = 'escape'
        self.escape_char = '\\'


class Comma(Token):
    def __init__(self):
        super().__init__()
        self.type = 'comma'


class Parenthesis(Token):
    def __init__(self, side):
        super().__init__()
        self.type = 'parenthesis'
        self.side = side


class LeftParenthesis(Parenthesis):
    def __init__(self):
        super().__init__(side='L')


class RightParenthesis(Parenthesis):
    def __init__(self):
        super().__init__(side='R')


class CurlyBrace(Token):
    def __init__(self, side):
        super().__init__()
        self.type = 'curly'
        self.side = side


class LeftCurlyBrace(CurlyBrace):
    def __init__(self):
        super().__init__(side='L')


class RightCurlyBrace(CurlyBrace):
    def __init__(self):
        super().__init__(side='R')


class Bracket(Token):
    def __init__(self, side):
        super().__init__()
        self.type = 'bracket'
        self.side = side


class LeftBracket(Bracket):
    def __init__(self):
        super().__init__(side='L')


class RightBracket(Bracket):
    def __init__(self):
        super().__init__(side='R')


class Quantifier(Token):
    def __init__(self, quantity, qtifier_char):
        super().__init__()
        self.type = 'qtifier'
        self.quantity = quantity
        self.qtifier_char = qtifier_char


class ZeroOrMore(Quantifier):
    def __init__(self, qtifier_char):
        super().__init__(quantity='zeroOrMore', qtifier_char=qtifier_char)


class OneOrMore(Quantifier):
    def __init__(self, qtifier_char):
        super().__init__(quantity='oneOrMore', qtifier_char=qtifier_char)


class ZeroOrOne(Quantifier):
    def __init__(self, qtifier_char):
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
    def __init__(self, or_ch):
        super().__init__()
        self.type = 'or'
        self.or_ch = or_ch


class VerticalBar(OrToken):
    def __init__(self):
        super().__init__(or_ch='|')


class NotToken(Token):
    def __init__(self, not_ch):
        super().__init__()
        self.type = 'not'
        self.not_ch = not_ch


class Circumflex(NotToken):
    def __init__(self):
        super().__init__(not_ch='^')


class Dash(Token):
    def __init__(self):
        super().__init__()
        self.type = 'dash'
        self.ch = '-'
