from typing import Union, Callable
from functools import lru_cache
import itertools
import math
from .lexer import Lexer
from .tokens import *
from .re_ast import *


class Pyrser:
    """ Regular Expression Parser.

    Pyrser instances can parse regular expressions and return the corresponding AST.    
    """

    def __init__(self) -> None:
        self.lxr = Lexer()

    @lru_cache(maxsize=4)
    def parse(self, re: str) -> RE:
        """ Parses a regular expression.

        Parses a regex and returns the corresponding AST.
        If the regex contains errors raises an Exception.

        Args:
            re (str): a regular expression

        Returns:
            RE: the root node of the regular expression's AST
        """

        def get_range_str(start: str, end: str) -> str:
            result = ''
            i = ord(start)
            while i <= ord(end):
                result += chr(i)
                i += 1
            return result

        def next_tkn_initializer(re: str) -> Callable[[bool], Union[Token, None]]:
            tokens = self.lxr.scan(re=re)

            i = -1

            def next_tkn(without_consuming: bool = False) -> Union[Token, None]:
                nonlocal i
                nonlocal tokens
                nonlocal curr_tkn

                if without_consuming:
                    return tokens[i+1] if len(tokens) > i+1 else None

                i += 1
                if i < len(tokens):
                    curr_tkn = tokens[i]
                else:
                    curr_tkn = None

            return next_tkn

        def parse_re() -> RE:
            return RE(parse_re_seq())

        def parse_re_seq(capturing: bool = True, group_name: str = None) -> Union[OrNode, GroupNode]:
            match_start, match_end = False, False
            if type(curr_tkn) is Start or type(curr_tkn) is Circumflex:
                next_tkn()
                match_start = True

            node = parse_group(capturing=capturing, group_name=group_name)

            if isinstance(curr_tkn, EndToken):
                next_tkn()
                match_end = True
            else:
                match_end = False

            if match_start:
                node.children.appendleft(StartElement())
            if match_end:
                node.children.append(EndElement())

            if isinstance(curr_tkn, OrToken):
                next_tkn()
                node = OrNode(left=node, right=parse_re_seq())

            return node

        def parse_group(capturing: bool = True, group_name: str = None) -> GroupNode:
            nonlocal groups_counter
            
            if group_name is None:
                group_name = "Group " + str(next(groups_counter))
            
            elements = deque()  # holds the children of the GroupNode

            while curr_tkn is not None and not isinstance(curr_tkn, OrToken) and \
                    not isinstance(curr_tkn, RightParenthesis) and \
                    not isinstance(curr_tkn, EndToken):
                new_el = parse_range_el()

                next_tkn()

                if isinstance(curr_tkn, EndToken):
                    elements.append(new_el)
                    break

                if isinstance(curr_tkn, Quantifier):
                    if isinstance(curr_tkn, ZeroOrOne):
                        new_el.min, new_el.max = 0, 1
                    elif isinstance(curr_tkn, ZeroOrMore):
                        new_el.min, new_el.max = 0, math.inf
                    else:
                        # suppose it's 1+
                        new_el.min, new_el.max = 1, math.inf
                    next_tkn()
                elif isinstance(curr_tkn, LeftCurlyBrace):
                    parse_curly(new_el)

                elements.append(new_el)
                # next_tkn()

            return GroupNode(children=elements, capturing=capturing, group_name=group_name)

        def parse_curly(new_el: ASTNode) -> None:
            # move past the left brace
            next_tkn()

            # find val_1, val_2
            val_1, val_2 = '', ''
            try:
                while isinstance(curr_tkn, ElementToken):
                    val_1 += curr_tkn.char
                    next_tkn()
                if val_1 == '':
                    val_1 == 0
                else:
                    val_1 = int(val_1)

                if isinstance(curr_tkn, RightCurlyBrace):
                    # I'm in the case {exact}
                    if type(val_1) is int:
                        new_el.min, new_el.max = val_1, val_1
                        next_tkn()  # skip the closing brace
                        return
                    else:
                        raise Exception()

                next_tkn()
                while isinstance(curr_tkn, ElementToken):
                    val_2 += curr_tkn.char
                    next_tkn()
                if val_2 == '':
                    val_2 == math.inf
                else:
                    val_2 = int(val_2)

                # skip the closing brace
                next_tkn()

                new_el.min = val_1 if type(val_1) is int else 0
                new_el.max = val_2 if type(val_2) is int else math.inf

            except Exception as e:
                raise Exception('Invalid curly brace syntax.')

        def parse_range_el() -> ASTNode:
            if isinstance(curr_tkn, LeftBracket):
                next_tkn()
                element = parse_inner_el()
                if isinstance(curr_tkn, RightBracket):
                    return element
                else:
                    raise Exception(
                        'Missing closing \']\'. Check the regex and try again.')
            else:
                return parse_el()

        def parse_inner_el() -> RangeElement:
            nonlocal curr_tkn
            # innerel creates a single RangeElement with all the matches
            match_str = ''
            if curr_tkn is None:
                raise Exception(
                    "Missing closing ']'. Check the regex and try again.")

            positive_logic = True
            if isinstance(curr_tkn, NotToken):
                positive_logic = False
                next_tkn()

            prev_char = None
            while curr_tkn is not None:
                if isinstance(curr_tkn, RightBracket):
                    break

                if isinstance(curr_tkn, SpaceToken):
                    match_str += curr_tkn.char
                    next_tkn()
                    continue

                # every character inside it must be treated as an element
                if not isinstance(curr_tkn, ElementToken):
                    curr_tkn = ElementToken(char=curr_tkn.char)

                if next_tkn(without_consuming=True) is None:
                    raise Exception(
                        "Missing closing ']'. Check the regex and try again.")
                elif isinstance(next_tkn(without_consuming=True), Dash):
                    # it may be a range (like a-z, A-M, 0-9, ...)
                    prev_char = curr_tkn.char
                    next_tkn()  # current token is now the Dash
                    if isinstance(next_tkn(without_consuming=True), RightBracket) or isinstance(next_tkn(without_consuming=True), SpaceToken):
                        # we're in one of these scenarios: "<char>-]" "<char>-\s"
                        # the dash and previous character must be interpreted as single elements
                        match_str += prev_char + curr_tkn.char
                    else:
                        # we're in the case of an actual range (or next_tkn is none)
                        next_tkn()  # curr_tkn is now the one after the dash
                        if next_tkn is None:
                            raise Exception(
                                "Missing closing ']'. Check the regex and try again.")
                        elif ord(prev_char) > ord(curr_tkn.char):
                            raise Exception(
                                f"Range values reversed. Start '{prev_char}' char code is greater than end '{curr_tkn.char}' char code.")
                        else:
                            match_str += get_range_str(prev_char,
                                                       curr_tkn.char)
                else:
                    # no range, no missing ']', just a char to add to match_str
                    match_str += curr_tkn.char
                next_tkn()

            return RangeElement(match_str="".join(sorted(set(match_str))), is_positive_logic=positive_logic)

        def parse_el() -> Union[Element, OrNode, GroupNode]:
            group_name: Union[str,None]
            group_name = None
            if isinstance(curr_tkn, ElementToken):
                return Element(match_ch=curr_tkn.char)
            elif isinstance(curr_tkn, Wildcard):
                return WildcardElement()
            elif isinstance(curr_tkn, SpaceToken):
                return SpaceElement()
            elif isinstance(curr_tkn, LeftParenthesis):
                next_tkn()
                # (?: for non-capturing group
                capturing = True
                if type(curr_tkn) is QuestionMark:
                    next_tkn()
                    if curr_tkn.char == ':':
                        capturing = False
                        next_tkn()
                    elif curr_tkn.char == '<':
                        next_tkn()
                        group_name = parse_group_name()
                    else:
                        if curr_tkn is None:
                            raise Exception('Unterminated group')
                        else:
                            raise Exception(
                                f'Invalid group: \'{LeftParenthesis()}{QuestionMark()}{curr_tkn.char}\'')
                res = parse_re_seq(capturing=capturing, group_name=group_name)
                if isinstance(curr_tkn, RightParenthesis):
                    # next_tkn() not needed (the parse_group while loop will eat the parenthesis)
                    return res
                else:
                    raise Exception('Missing closing group parenthesis \')\'')
            else:
                raise Exception(
                    'Unescaped special character {}'.format(curr_tkn.char))

        def parse_group_name() -> str:
            if curr_tkn is None:
                raise Exception('Unterminated named group name.')
            group_name = ''
            while curr_tkn.char != '>':
                group_name += curr_tkn.char
                next_tkn()
                if curr_tkn is None:
                    raise Exception('Unterminated named group name.')
            if len(group_name) == 0:
                raise Exception('Unexpected empty named group name.')
            next_tkn()  # consumes '>'
            return group_name
        
        groups_counter = itertools.count(start=1)

        curr_tkn = None
        next_tkn = next_tkn_initializer(re)
        next_tkn()

        ast = parse_re()
        if curr_tkn is not None:
            raise Exception(
                "Unable to parse the entire regex.\nCheck the regex and try again.")
        return ast
