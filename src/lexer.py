from .tokens import *
import numpy as np


class Lexer:
    def __init__(self):
        self.__digits__ = '0123456789'
        pass

    def __is_digit__(self, ch):
        return self.__digits__.find(ch) > -1

    def scan(self, re: str):
        tokens = np.array([])

        def append(elem):
            nonlocal tokens
            tokens = np.append(tokens, elem)

        i = 0
        escape_found = False
        while i < len(re):
            ch = re[i]
            if escape_found:
                if ch == 't':
                    append(ElementToken(char='\t'))
                else:
                    append(ElementToken(char=ch))
            elif ch == '\\':
                escape_found = True
                i += 1  # otherwise i won't be incremented bc of continue
                continue
            elif ch == '.':
                append(Wildcard())
            elif ch == '(':
                append(LeftParenthesis())
            elif ch == ')':
                append(RightParenthesis())
            elif ch == '[':
                append(LeftBracket())
            elif ch == '-':
                append(Dash())
            elif ch == ']':
                append(RightBracket())
            elif ch == '{':
                append(LeftCurlyBrace())
                i += 1
                while i < len(re):
                    ch = re[i]
                    if ch == ',':
                        append(Comma())
                    elif self.__is_digit__(ch):
                        append(ElementToken(char=ch))
                    elif ch == '}':
                        append(RightCurlyBrace())
                        break
                    else:
                        raise Exception('Bad token at index ${}.'.format(i))
                    i += 1
            elif ch == '^':
                if i == 0:
                    append(Start())
                else:
                    append(Circumflex())
            elif ch == '$':
                append(End())
            elif ch == '?':
                append(QuestionMark())
            elif ch == '*':
                append(Asterisk())
            elif ch == '+':
                append(Plus())
            elif ch == '|':
                append(VerticalBar())
            elif ch == '}':
                append(RightCurlyBrace())
            else:
                append(ElementToken(char=ch))

            escape_found = False
            i += 1

        return tokens
