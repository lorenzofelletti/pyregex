import numpy as np
from .lexer import Lexer
from .tokens import *
from .re_ast import *


class Pyrser:
    """
    Pyrser parse regular expressions and return the correspondent AST.

    Legal Regex examples:
    a
    (a)
    a|b
    ^a[^0-3b-xz]|BBBA{3,4}$
    ^\?.*VR|46.+e?$
    """

    def __init__(self):
        self.lxr = Lexer()

    def parse(self, re: str):
        """
        REGEX GRAMMAR recognized:
        RE ::= RE_SEQ
        RE_SEQ ::= '^'? GROUP '$'? ('|' RE_SEQ)?
        GROUP ::= (RANGE_EL QTIFIER?)+
        RANGE_EL ::= EL | '[' '^'? INNER_EL ']'
        EL ::= '\\'? (ch | SPECIAL) | '(' ('?:')? RE_SEQ ')'

        QTIFIER ::= '*' | '+' | '?' | '{' (num)? ',' num '}' | '{' num '}'
        INNER_EL ::= ch+ | ch '-' ch INNER_EL
        SPECIAL ::= '(' | ')' | '+' | '{' | '[' | '|' | '.' | '^' | '$' | ...
        """
        #lower_alphabet_characters = 'abcdefghijklmnopqrstuvwxyz'
        #upper_alphabet_characters = lower_alphabet_characters.upper()
        #digit_characters = '0123456789'

        def get_range_str(start: str, end: str):
            result = ''
            i = ord(start)
            while i <= ord(end):
                result += chr(i)
                i += 1
            return result

        # def get_range_str(original_str, idx1, idx2):
            # if not negate:
        #    return original_str[idx1:idx2+1]
            # else:
            #    return original_str[:idx1] + original_str[idx2+1:]

        def next_tkn_initializer(re: str):
            tokens = self.lxr.scan(re=re)

            i = -1

            def next_tkn(without_consuming: bool = False):
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

        def parse_re():
            return RE(parse_re_seq())

        def parse_re_seq(capturing: bool = True):
            match_start, match_end = False, False
            if type(curr_tkn) is Start or type(curr_tkn) is Circumflex:
                next_tkn()
                match_start = True

            node = parse_group(capturing=capturing)

            if isinstance(curr_tkn, EndToken):
                next_tkn()
                match_end = True
            else:
                match_end = False

            if match_start:
                node.children = np.append(StartElement(), node.children)
            if match_end:
                node.children = np.append(node.children, EndElement())

            if isinstance(curr_tkn, OrToken):
                next_tkn()
                node = OrNode(left=node, right=parse_re_seq())

            return node

        def parse_group(capturing: bool = True):
            elements = np.array([])  # holds the children of the GroupNode

            while curr_tkn is not None and not isinstance(curr_tkn, OrToken) and \
                    not isinstance(curr_tkn, RightParenthesis) and \
                    not isinstance(curr_tkn, EndToken):
                new_el = parse_range_el()

                next_tkn()

                if isinstance(curr_tkn, EndToken):
                    elements = np.append(elements, new_el)
                    break

                if isinstance(curr_tkn, Quantifier):
                    if isinstance(curr_tkn, ZeroOrOne):
                        new_el.min, new_el.max = 0, 1
                    elif isinstance(curr_tkn, ZeroOrMore):
                        new_el.min, new_el.max = 0, np.inf
                    else:
                        # suppose it's 1+
                        new_el.min, new_el.max = 1, np.inf
                    next_tkn()
                elif isinstance(curr_tkn, LeftCurlyBrace):
                    parse_curly(new_el)

                elements = np.append(elements, new_el)
                # next_tkn()

            return GroupNode(children=elements, capturing=capturing)

        def parse_curly(new_el: ASTNode):
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
                    val_2 == np.inf
                else:
                    val_2 = int(val_2)

                # skip the closing brace
                next_tkn()

                new_el.min = val_1 if type(val_1) is int else 0
                new_el.max = val_2 if type(val_2) is int else np.inf

            except Exception as e:
                raise Exception('Invalid curly brace syntax.')

        def parse_range_el():
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

        def parse_inner_el():
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

        def parse_el():
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
                    if type(curr_tkn) is ElementToken and curr_tkn.char == ':':
                        capturing = False
                        next_tkn()
                    else:
                        if curr_tkn is None:
                            raise Exception('Unterminated Group')
                        else:
                            raise Exception(
                                f'Invalid group: \'{LeftParenthesis()}{QuestionMark()}{curr_tkn.char}\'')
                res = parse_re_seq(capturing=capturing)
                if isinstance(curr_tkn, RightParenthesis):
                    # next_tkn() not needed (the parse_group while loop will eat the parenthesis)
                    return res
                else:
                    raise Exception('Missing closing group parenthesis \')\'')
            else:
                raise Exception(
                    'Unescaped special character {}'.format(curr_tkn.char))

        curr_tkn = None
        next_tkn = next_tkn_initializer(re)
        next_tkn()

        ast = parse_re()
        if curr_tkn is not None:
            raise Exception(
                "Unable to parse the entire regex.\nCheck the regex and try again.")
        return ast
