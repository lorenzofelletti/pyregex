from typing import List
from functools import lru_cache
from .tokens import *


class Lexer:
    """ Lexer for the pyregexp library.

    This class contains the method to scan a regular expression string producing the corresponding tokens.
    """

    def __init__(self) -> None:
        self.__digits__ = '0123456789'

    def __is_digit__(self, ch: str) -> bool:
        return self.__digits__.find(ch) > -1

    @lru_cache(maxsize=4)
    def scan(self, re: str) -> List[Token]:
        """ Regular expressions scanner.

        Scans the regular expression in input and produces the list of recognized Tokens in output.
        It raises an Exception if there are errors in the regular expression.

        Args:
            re (str): the regular expression to scan

        Returns:
            List[Token]: the list of tokens recognized in the passed regex
        """
        tokens = []

        def append(elem: Token) -> None:
            nonlocal tokens
            tokens.append(elem)

        i = 0
        escape_found = False
        while i < len(re):
            ch = re[i]
            if escape_found:
                if ch == 't':
                    append(ElementToken(char='\t'))
                if ch == 's':
                    # \s matches a space character
                    append(SpaceToken(space_ch=ch))
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
