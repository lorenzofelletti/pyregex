from collections import deque
import itertools
from typing import Deque


class ASTNode:
    """ AST nodes base class.

    Abstract Syntax Tree classes hierarchy base class.
    """
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(ASTNode.id_iter)
        self.type = 'astNode'


class RE(ASTNode):
    """ Entry point of the AST.

    This class acts as the entry point for a regular expression's AST.
    """

    def __init__(self, child: ASTNode, capturing: bool = False, group_name: str = "RegEx"):
        super().__init__()
        self.type = 're'
        self.__capturing__ = capturing
        self.group_name = group_name
        self.child = child
        self.children = deque([child])

    def is_capturing(self):
        return self.__capturing__


class LeafNode(ASTNode):
    """ AST class defining the leaf nodes.

    Every leaf node inherits from this class. 
    """

    def __init__(self) -> None:
        super().__init__()

    def is_match(self, ch: str = None, str_i: int = None, str_len: int = None) -> bool:
        """
        Returns whether the passed inputs matches with the node.

        For example, if the node matches the character "a" and the passed ch is
        "b" the method will return False, but if the passed ch was "a" then the
        result would have been True.

        Args:
            ch (str): the char you want to match
            str_i (int): the string index you are considering
            str_len (int): the test string length

        Returns:
            bool: represents whether there is a match between the node and the
            passed parameters or not.
        """
        return False


class Element(LeafNode):
    """ AST Element.

    Specialization of the LeafNode class. This class models the elements of a regex.
    """

    def __init__(self, match_ch: str = None) -> None:
        super().__init__()
        self.type = 'element'
        self.match = match_ch
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        return self.match == ch


class WildcardElement(Element):
    """ AST WildcardElement.

    Specialization of the Element class to model the wildcard behavior.
    """

    def __init__(self) -> None:
        super().__init__(match_ch='anything')
        self.type = 'wildcardElement'
        self.match = None

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        return ch != '\n'


class SpaceElement(Element):
    """ AST SpaceElement.

    Specialization of the element class to model the match-space behavior.
    """

    def __init__(self) -> None:
        super().__init__()
        self.type = 'spaceElement'
        self.match = None

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        return ch.isspace() and len(ch) == 1


class RangeElement(LeafNode):
    """ AST RangeElement.

    Specialization of the LeafNode class modeling the range-element behavior,
    that is that it matches with more than one character.
    """

    def __init__(self, match_str: str, is_positive_logic: bool = True) -> None:
        super().__init__()
        self.type = 'rangeElement'
        self.match = match_str
        self.min = 1
        self.max = 1
        self.is_positive_logic = is_positive_logic

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        # XNOR of whether the ch is found and the logic (positive/negative)
        return not((ch in self.match) ^ self.is_positive_logic)


class StartElement(LeafNode):
    """ AST StartElement.

    Inherits from LeafNode and models the match-start-element behavior.
    """

    def __init__(self) -> None:
        super().__init__()
        self.type = 'startElement'
        self.match = None
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        return str_i == 0


class EndElement(LeafNode):
    """ AST EndElement.

    Inherits from LeafNode and models the match-end-element behavior.
    """

    def __init__(self) -> None:
        super().__init__()
        self.type = 'endElement'
        self.match = ''
        self.min = 1
        self.max = 1

    def is_match(self, ch: str = None, str_i: int = 0, str_len: int = 0) -> bool:
        return str_i == str_len


class OrNode(ASTNode):
    """ AST OrNode.

    Inherits from ASTNode and models the or-nodes, that is the nodes that
    divides the regex into two possible matching paths.
    """

    def __init__(self, left: ASTNode, right: ASTNode) -> None:
        super().__init__()
        self.type = 'orNode'
        self.left = left
        self.right = right
        self.children = [left, right]
        self.min = 1
        self.max = 1


# unused
class NotNode(ASTNode):
    """ AST NotNode.

    Inherits from ASTNode and models the not-node behavior.
    """

    def __init__(self, child: ASTNode) -> None:
        super().__init__()
        self.type = 'notNode'
        self.child = child
        self.children = deque([child])


class GroupNode(ASTNode):
    """ AST GroupNode.

    Inherits from ASTNode and models the group in a regex.
    """

    def __init__(self, children: Deque[ASTNode], capturing: bool = False, group_name: str = 'default') -> None:
        super().__init__()
        self.type = 'groupNode'
        self.__capturing__ = capturing
        self.group_name = group_name
        self.children = children
        self.min = 1
        self.max = 1

    def is_capturing(self) -> bool:
        """ Returns whether the GroupNode is capturing.

        Returns:
            bool: True if the group is capturing, False otherwise
        """
        return self.__capturing__
