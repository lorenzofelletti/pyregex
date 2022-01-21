import numpy as np


class ASTNode:
    """
    Abstract Syntax Tree classes hierarchy base class.
    """

    def __init__(self):
        self.type = 'astNode'
        self.__capturing__ = None

    def is_capturing(self):
        return self.__capturing__


class RE(ASTNode):
    """
    AST class entry point for a regular expression's AST.
    """

    def __init__(self, child):
        super().__init__()
        self.type = 're'
        # self.__capturing__ = True
        self.child = child
        self.children = [child]

    # def is_capturing(self):
    #    return self.__capturing__


class LeafNode(ASTNode):
    """
    AST class defining the concept of leaf node.
    Every leaf node inherits from this class. 
    """

    def __init__(self):
        super().__init__()

    def is_match(self, ch: str):
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

    def is_match(self, ch: str):
        return self.match == ch


class WildcardElement(Element):
    """
    Specialization of the Element class to model the wildcard behavior.
    """

    def __init__(self):
        super().__init__(match_ch='anything')
        self.type = 'wildcard_element'
        self.match = True

    def is_match(self, ch: str):
        return ch != '\n'


class SpaceElement(Element):
    """
    Specialization of the element class to model the match-space behavior.
    """

    def __init__(self):
        super().__init__('apce')
        self.type = 'spaceElement'
        self.match = True

    def is_match(self, ch: str):
        return ch.isspace() and len(ch) == 1


class RangeElement(LeafNode):
    """
    Specialization of the LeafNode class modeling the range-element behavior,
    that is that it matches with more than one character.
    """

    def __init__(self, match_str: str):
        super().__init__()
        self.type = 'rangeElement'
        self.match = match_str
        self.min = 1
        self.max = 1

    def is_match(self, ch: str):
        return self.match.find(ch)


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


class OrNode(ASTNode):
    """
    Inherits from ASTNode and models the or-nodes, that is the nodes that
    divides the regex into two possible matching paths.
    """

    def __init__(self, left, right):
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

    def __init__(self, child):
        super().__init__()
        self.type = 'notNode'
        self.child = child
        self.children = [child]


class GroupNode(ASTNode):
    """
    Inherits from ASTNode and models the group in a regex.
    """

    def __init__(self, children, capturing=False):
        super().__init__()
        self.type = 'groupNode'
        self.__capturing__ = capturing
        self.children = children
        self.min = 1
        self.max = 1

    def is_capturing(self):
        return self.__capturing__
