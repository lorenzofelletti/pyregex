from collections import deque
import itertools
import typing


class ASTNode:
    """
    Abstract Syntax Tree classes hierarchy base class.
    """
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(ASTNode.id_iter)
        self.type = 'astNode'
        self.__capturing__ = None

    def is_capturing(self):
        return self.__capturing__


class RE(ASTNode):
    """
    AST class entry point for a regular expression's AST.
    """

    def __init__(self, child: ASTNode):
        super().__init__()
        self.type = 're'
        # self.__capturing__ = True
        self.child = child
        self.children = deque([child])

    # def is_capturing(self):
    #    return self.__capturing__


class LeafNode(ASTNode):
    """
    AST class defining the concept of leaf node.
    Every leaf node inherits from this class. 
    """

    def __init__(self):
        super().__init__()

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        """
        Returns a tuple of if a match were found, and how many characters were matched.
        The parameters to be passed are:
         * str: the (whole) test string
         * str_i: the current consumed characters (of str) index.
        """
        return False


class Element(LeafNode):
    """
    Specialization of the LeafNode class. This class models the elements of a regex.
    """

    def __init__(self, match_ch: str):
        super().__init__()
        self.type = 'element'
        self.match = match_ch
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        return self.match == ch


class WildcardElement(Element):
    """
    Specialization of the Element class to model the wildcard behavior.
    """

    def __init__(self):
        super().__init__(match_ch='anything')
        self.type = 'wildcard_element'
        self.match = True

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        return ch != '\n'


class SpaceElement(Element):
    """
    Specialization of the element class to model the match-space behavior.
    """

    def __init__(self):
        super().__init__('apce')
        self.type = 'spaceElement'
        self.match = True

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        return ch.isspace() and len(ch) == 1


class RangeElement(LeafNode):
    """
    Specialization of the LeafNode class modeling the range-element behavior,
    that is that it matches with more than one character.
    """

    def __init__(self, match_str: str, is_positive_logic: bool = True):
        super().__init__()
        self.type = 'rangeElement'
        self.match = match_str
        self.min = 1
        self.max = 1
        self.is_positive_logic = is_positive_logic

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        # XNOR of whether the ch is found and the logic (positive/negative)
        return not((ch in self.match) ^ self.is_positive_logic)


class StartElement(LeafNode):
    """
    Inherits from LeafNode and models the match-start-element behavior.
    """

    def __init__(self):
        super().__init__()
        self.type = 'startElement'
        self.match = 0
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        return str_i == 0


class EndElement(LeafNode):
    """
    Inherits from LeafNode and models the match-end-element behavior.
    """

    def __init__(self):
        super().__init__()
        self.type = 'endElement'
        self.match = 'len(string)'
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = ' ', str_i: int = 0, str_len: int = 0):
        return str_i == str_len


class OrNode(ASTNode):
    """
    Inherits from ASTNode and models the or-nodes, that is the nodes that
    divides the regex into two possible matching paths.
    """

    def __init__(self, left: ASTNode, right: ASTNode):
        super().__init__()
        self.type = 'orNode'
        self.left = left
        self.right = right
        self.children = [left, right]
        self.min = 1
        self.max = 1


# unused
class NotNode(ASTNode):
    """
    Inherits from ASTNode and models the not-node behavior.
    """

    def __init__(self, child: ASTNode):
        super().__init__()
        self.type = 'notNode'
        self.child = child
        self.children = deque([child])


class GroupNode(ASTNode):
    """
    Inherits from ASTNode and models the group in a regex.
    """

    def __init__(self, children: typing.Deque[ASTNode], capturing: bool = False, group_name: str = 'default'):
        super().__init__()
        self.type = 'groupNode'
        self.__capturing__ = capturing
        self.group_name = group_name
        self.children = children
        self.min = 1
        self.max = 1

    def is_capturing(self) -> bool:
        return self.__capturing__
