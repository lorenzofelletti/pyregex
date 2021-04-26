class ASTNode:
    pass


class RE(ASTNode):
    def __init__(self, child):
        super().__init__()
        self.type = 're'
        self.child = child
        self.match_start = False
        self.match_end = False


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


class NotNode(ASTNode):
    def __init__(self, child):
        super().__init__()
        self.type = 'notNode'
        self.child = child


class GroupNode(ASTNode):
    def __init__(self, children):
        super().__init__()
        self.type = 'groupNode'
        self.children = children
        self.min = 1
        self.max = 1
