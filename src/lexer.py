from .tokens import *
import numpy as np


class Lexer:
    def __init__(self):
        self.__digits__ = '0123456789'
        pass

    def __is_digit__(self, ch):
        return self.__digits__.find(ch) > -1

    def scan(self, re):
        tokens = np.array([])

        def append(elem):
            nonlocal tokens
            tokens = np.append(tokens, elem)

        i = 0
        escape_found = False
        while i < len(re):
            ch = re[i]
            if escape_found:
                i += 1
                append(Element(char=re[i]))
            elif ch == '\\':
                escape_found = True
                continue
            elif ch == '.':
                append(Wildcard())
            elif ch == '(':
                append(LeftParenthesis())
            elif ch == ')':
                append(RightParenthesis())
            elif ch == '[':
                append(LeftBracket())
            elif ch == ']':
                append(RightBracket())
            elif ch == '{':
                append(LeftCurlyBrace())
                while i < len(re):
                    ch = re[i]
                    if ch == ',':
                        append(Comma())
                    elif self.__is_digit__(ch):
                        append(Element(char=ch))
                    elif ch == '}':
                        append(RightCurlyBrace())
                        break
                    else:
                        raise Exception('Bad token at index ${:d}.'.format(i))
                    i += 1
            elif ch == '^':
                append(Start())
            elif ch == '$':
                append(End())
            else:
                append(Element(char=ch))

            escape_found = False
            i += 1
        
        return tokens
