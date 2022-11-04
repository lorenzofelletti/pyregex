from typing import List
from .tokens import *
from .exceptions import BadCurlyQuantifierException, BadTokenException


direct_char_to_token = {
    '.': Wildcard,
    '$': End,
    '[': LeftBracket,
    ']': RightBracket,
    '(': LeftParenthesis,
    ')': RightParenthesis,
    '-': Dash,
    '|': VerticalBar,
    '?': QuestionMark,
    '*': Asterisk,
    '+': Plus,
}

raise_exception_chars = {
    '}', BadTokenException,
}

class Lexer:
    """ Lexer for the pyregexp library.

    This class contains the method to scan a regular expression string producing the corresponding tokens.
    """

    def __init__(self) -> None:
        self.__digits__ = '0123456789'
        self.tokens = []

    def __is_digit__(self, ch: str) -> bool:
        return self.__digits__.find(ch) > -1

    def __append__(self, elem: Token) -> None:
            self.tokens.append(elem)

    def __scan_curly_quantifier__(self, regex: str, index: int) -> int:
        """ Scans the curly quantifier in the regular expression.

        Args:
            regex (str): the regular expression to scan
            index (int): the index of the first character of the curly quantifier

        Returns:
            int: the index of the last character of the curly quantifier
        """
        i = index
        self.__append__(LeftCurlyBrace())
        i += 1
        while i < len(regex):
            ch = regex[i]
            if ch == ',':
                self.__append__(Comma())
            elif self.__is_digit__(ch):
                self.__append__(ElementToken(char=ch))
            elif ch == '}':
                self.__append__(RightCurlyBrace())
                break
            else:
                raise BadCurlyQuantifierException(f"Bad token at index ${i}.")
            i += 1

        return i
    
    def __handle_escape__(self, ch: str) -> None:
        """ Handles the escape character.

        Args:
            ch (str): the character to handle
        """
        if ch == 't':
            self.__append__(ElementToken(char='\t'))
        elif ch == 's':
            self.__append__(SpaceToken(char=ch))
        else:
            self.__append__(ElementToken(char=ch))

    def scan(self, re: str) -> List[Token]:
        """ Regular expressions scanner.

        Scans the regular expression in input and produces the list of recognized Tokens in output.
        It raises an Exception if there are errors in the regular expression.

        Args:
            re (str): the regular expression to scan

        Returns:
            List[Token]: the list of tokens recognized in the passed regex
        """
        self.tokens = []

        i = 0
        escape_found = False
        while i < len(re):
            ch = re[i]
            if escape_found:
                self.__handle_escape__(ch)
                escape_found = False
            elif ch == '\\':
                escape_found = True
            elif ch in direct_char_to_token:
                self.__append__(direct_char_to_token[ch]())
            elif ch == '{':
                i = self.__scan_curly_quantifier__(re, i)
            elif ch == '^':
                if i == 0:
                    self.__append__(Start())
                else:
                    self.__append__(Circumflex())
            elif ch in raise_exception_chars:
                raise BadTokenException(f"Bad token at index ${i}.")
            else:
                self.__append__(ElementToken(char=ch))

            i += 1

        return self.tokens
