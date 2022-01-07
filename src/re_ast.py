import numpy as np


class ASTNode:
    """
    Abstract Syntax Tree classes hierarchy base class.
    """
    pass


class RE(ASTNode):
    """
    AST class entry point for a regular expression's AST.
    """

    def __init__(self, child):
        super().__init__()
        self.type = 're'
        self.child = child
        self.children = [child]


class LeafNode(ASTNode):
    """
    AST class defining the concept of leaf node.
    Every leaf node inherits from this class. 
    """

    def __init__(self):
        super().__init__()


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


class WildcardElement(Element):
    """
    Specialization of the Element class to model the wildcard behavior.
    """

    def __init__(self):
        super().__init__(match_ch='anything')
        self.type = 'wildcard_element'
        self.match = True


class SpaceElement(Element):
    """
    Specialization of the element class to model the match-space behavior.
    """

    def __init__(self, match_ch: str):
        super().__init__(match_ch)
        self.type = 'space_element'
        self.match = ' \t'
        self.min = 1
        self.max = np.inf


class RangeElement(LeafNode):
    """
    Specialization of the LeafNode class modeling the range-element behavior,
    that is that it matches with more than one character.
    """

    def __init__(self, match_str):
        super().__init__()
        self.type = 'rangeElement'
        self.match = match_str
        self.min = 1
        self.max = 1


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

    def __init__(self, children):
        super().__init__()
        self.type = 'groupNode'
        self.children = children
        self.min = 1
        self.max = 1
