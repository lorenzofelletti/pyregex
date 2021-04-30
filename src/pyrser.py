import numpy as np
from .lexer import Lexer
from .tokens import *
from .re_ast import *
# np.inf infinite representations


class Pyrser:
    """
    Pyrser parse regular expressions and return the correspondent AST.

    Legal Regex examples:
    a
    (a)
    a|b
    ^a[^0-3|b-z|^cd]|BBBA{3,4}$
    ^\?.*VR|46.+e?$
    """

    def __init__(self):
        self.lxr = Lexer()

    def parse(self, re):
        """
        REGEX GRAMMAR recognized:
        RE ::= '^'? RE_SEQ | '$'
        RE_SEQ ::= GROUP ('|' RE_SEQ)?
        GROUP ::= (RANGE_EL QTIFIER?)*
        RANGE_EL= EL | '[' INNER_EL ']'
        EL ::= '\\'? (ch | SPECIAL) | '(' RE_SEQ ')'

        QTIFIER ::= '*' | '+' | '?' | '{' (num, ',')? num '}'
        INNER_EL ::= BASE_EL+ | BASE_EL '-' BASE_EL ('|' INNER_EL)*
        SPECIAL ::= '(' | ')' | '+' | '{' | '[' | '|' | '.' | '^' | '$' | ...
        """
        alphabet_characters = 'abcdefghijklmnopqrstuvwxyz'
        digit_characters = '0123456789'

        def get_range_str(original_str, idx1, idx2, negate):
            if not negate:
                return original_str[idx1:idx2+1]
            else:
                return original_str[:idx1] + original_str[idx2+1:]

        def next_tkn_initializer(re):
            tokens = self.lxr.scan(re=re)

            i = -1

            def next_tkn():
                nonlocal i
                nonlocal tokens
                nonlocal curr_tkn
                i += 1
                if i < len(tokens):
                    curr_tkn = tokens[i]
                else:
                    curr_tkn = None

            return next_tkn

        def parse_re():
            match_start, match_end = True, True
            if isinstance(curr_tkn, StartToken):
                next_tkn()
            else:
                match_start = False

            node = RE(parse_re_seq())

            if isinstance(curr_tkn, EndToken):
                next_tkn()
            else:
                match_end = False

            if not match_start:
                any_at_start = WildcardElement()
                any_at_start.min, any_at_start.max = 0, np.inf
                if type(node.child) is GroupNode:
                    node.child.children = np.insert(
                        node.child.children, 0, any_at_start)
                    node.children = [node.child]
                else:
                    # is OrNode
                    new_re_child = GroupNode(
                        children=np.array([any_at_start, node.child]))
                    node.child = new_re_child
                    node.children = [node.child]

            if not match_end:
                any_at_end = WildcardElement()
                any_at_end.min, any_at_end.max = 0, np.inf
                if type(node.child) is GroupNode:
                    node.child.children = np.append(
                        node.child.children, any_at_end)
                    node.children = [node.child]
                else:
                    new_re_child = GroupNode(
                        children=np.array([node.child, any_at_end]))
                    node.child = new_re_child
                    node.children = [node.child]

            return node

            if match_start:
                RE.match_start = True
            if match_end:
                RE.match_end = True

        def parse_re_seq():
            elements = parse_group()
            while isinstance(curr_tkn, OrToken):
                next_tkn()
                elements = OrNode(left=elements, right=parse_group())
            return elements

        def parse_group():
            elements = np.array([])  # holds the children of the GroupNode

            while curr_tkn is not None and not isinstance(curr_tkn, OrToken) and not isinstance(curr_tkn, RightParenthesis):
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

                if isinstance(curr_tkn, LeftCurlyBrace):
                    next_tkn()
                    if isinstance(curr_tkn, ElementToken):
                        val_1 = int(curr_tkn.char)

                        next_tkn()
                        if isinstance(curr_tkn, Comma):
                            next_tkn()
                            if isinstance(curr_tkn, Element):
                                val_2 = int(curr_tkn.char)
                                new_el.min, new_el.max = val_1, val_2

                                next_tkn()
                                if not isinstance(curr_tkn, RightCurlyBrace):
                                    raise Exception(
                                        'Invalid curly brace syntax.\nUse one of the legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')
                            elif isinstance(curr_tkn, RightCurlyBrace):
                                new_el.min = val_1
                                new_el.max = np.inf
                            else:
                                raise Exception(
                                    'Invalid curly brace syntax.\nUse one of the legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')
                        elif isinstance(curr_tkn, RightCurlyBrace):
                            new_el.min, new_el.max = val_1, val_1
                        else:
                            raise Exception(
                                'Invalid curly brace syntax.\nUse one of the legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')

                    elif isinstance(curr_tkn, Comma):
                        new_el.min = 0
                        next_tkn()
                        if isinstance(curr_tkn, Element):
                            new_el.max = int(curr_tkn.char)
                            next_tkn()
                            if not isinstance(curr_tkn, RightCurlyBrace):
                                raise Exception(
                                    'Invalid curly brace syntax.\nUse one of the legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')
                        else:
                            raise Exception(
                                'Invalide curly brace syntax.\nUse one of the legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')

                    else:
                        raise Exception(
                            'Escape the \'{\'curly brace or use one of the following legal syntaxes:\n\t{min,max}\n\t{min,}\n\t{,max}')
                    next_tkn()

                elements = np.append(elements, new_el)
                # next_tkn()

            return GroupNode(children=elements)

        def parse_range_el():
            if isinstance(curr_tkn, LeftBracket):
                next_tkn()
                element = parse_inner_el()
                if isinstance(curr_tkn, RightBracket):
                    return element
                else:
                    raise Exception(
                        'Missing closing \']\'. Correct the regex and try again.')
            else:
                return parse_el()

        def parse_inner_el():
            # innerel creates a single RangeElement with all the matches
            match_str = ''
            if curr_tkn is None:
                raise Exception("Missing ']'. Check the regex and try again.")

            tkn1 = None
            tkn2 = None
            while curr_tkn is not None and not isinstance(curr_tkn, RightBracket):
                negate = False

                tkn1 = curr_tkn

                if isinstance(curr_tkn, OrToken):
                    tkn1 = None
                    next_tkn()
                    continue

                if isinstance(curr_tkn, NotToken):
                    negate = True
                    next_tkn()
                    tkn1 = curr_tkn

                if isinstance(tkn1, ElementToken):
                    next_tkn()
                    tkn2 = curr_tkn
                    if isinstance(tkn2, RightBracket):
                        break
                    elif isinstance(tkn2, ElementToken):
                        match_str += tkn1.char + tkn2.char
                    elif isinstance(tkn2, Dash):
                        next_tkn()
                        tkn2 = curr_tkn
                        if not isinstance(tkn2, ElementToken):
                            raise Exception(
                                'Expected a character token, instead got a {:s}'.format(type(tkn2)))

                        if alphabet_characters.lower().find(tkn1.char) > -1 and \
                                alphabet_characters.lower().find(tkn2.char) > -1:
                            idx1 = alphabet_characters.lower().find(tkn1.char)
                            idx2 = alphabet_characters.lower().find(tkn2.char)
                            match_str += get_range_str(
                                alphabet_characters.lower(), idx1, idx2, negate)
                        elif alphabet_characters.upper().find(tkn1.char) > -1 and \
                                alphabet_characters.upper().find(tkn2.char) > -1:
                            idx1 = alphabet_characters.upper().find(tkn1.char)
                            idx2 = alphabet_characters.upper().find(tkn2.char)
                            match_str += get_range_str(
                                alphabet_characters.upper(), idx1, idx2, negate)
                        elif digit_characters.find(tkn1.char) > -1 and \
                                digit_characters.find(tkn2.char) > -1:
                            idx1 = digit_characters.find(tkn1.char)
                            idx2 = digit_characters.find(tkn2.char)
                            match_str += get_range_str(digit_characters,
                                                       idx1, idx2, negate)
                        else:
                            raise Exception(
                                'Unable to parse the range {}-{}'.format(tkn1.char, tkn2.char))

                next_tkn()
                tkn1 = None
                tkn2 = None

            if isinstance(tkn1, ElementToken):
                match_str += tkn1.char

            return RangeElement(match_str="".join(sorted(set(match_str))))

        def parse_el():
            if isinstance(curr_tkn, ElementToken):
                return Element(match_ch=curr_tkn.char)
            elif isinstance(curr_tkn, Wildcard):
                return WildcardElement()
            elif isinstance(curr_tkn, LeftParenthesis):
                next_tkn()
                res = parse_re_seq()
                if isinstance(curr_tkn, RightParenthesis):
                    # next_tkn() not needed (the parse_group while loop will eat the parenthesis)
                    return res
                else:
                    raise Exception('Missing closing group parenthesis \')\'')
            else:
                return

        curr_tkn = None
        next_tkn = next_tkn_initializer(re)
        next_tkn()
        return parse_re()
