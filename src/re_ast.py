class ASTNode:
    pass


class RE(ASTNode):
    def __init__(self, child):
        super().__init__()
        self.type = 're'
        self.child = child
        self.children = [child]


class LeafNode(ASTNode):
    def __init__(self):
        super().__init__()


class Element(LeafNode):
    def __init__(self, match_ch):
        super().__init__()
        self.type = 'element'
        self.match = match_ch
        self.min = 1
        self.max = 1


class WildcardElement(Element):
    def __init__(self):
        super().__init__(match_ch='anything')
        self.type = 'wildcard_element'
        self.match = True


class RangeElement(LeafNode):
    def __init__(self, match_str):
        super().__init__()
        self.type = 'rangeElement'
        self.match = match_str
        self.min = 1
        self.max = 1


class OrNode(ASTNode):
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
    def __init__(self, child):
        super().__init__()
        self.type = 'notNode'
        self.child = child
        self.children = [child]


class GroupNode(ASTNode):
    def __init__(self, children):
        super().__init__()
        self.type = 'groupNode'
        self.children = children
        self.min = 1
        self.max = 1
