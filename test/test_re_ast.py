from ..pyregexp.re_ast import ASTNode, RE, LeafNode, Element, WildcardElement, SpaceElement, RangeElement, StartElement, EndElement, OrNode, NotNode, GroupNode


def test_ast_node():
    ast_node = ASTNode()
    assert ast_node is not None


def test_re():
    re = RE(child=Element(match_ch='e'))
    assert re is not None

    assert hasattr(re, 'child')
    assert hasattr(re, 'children')

    assert re.child is re.children[0]


def test_not_node():
    not_node = NotNode(child=Element(match_ch='e'))
    assert not_node is not None

    assert hasattr(not_node, 'child')
    assert hasattr(not_node, 'children')

    assert not_node.child is not_node.children[0]


def test_leaf_node():
    ln = LeafNode()
    assert ln is not None
    assert hasattr(ln, 'is_match')

    assert ln.is_match() == False


def test_wildcard_element():
    we = WildcardElement()
    assert we is not None


def test_space_element():
    se = SpaceElement()
    assert se is not None
    assert hasattr(se, 'is_match')

    assert se.is_match(" ")
    assert se.is_match("\t")
    assert se.is_match("\n")
    assert se.is_match("\f")
    assert se.is_match("\r")
    assert se.is_match("t") == False


def test_range_element_positive_logic():
    re = RangeElement("abc", True)
    assert re is not None
    assert re.is_positive_logic == True

    assert re.is_match("a") == True
    assert re.is_match("x") == False


def test_range_element_negative_logic():
    nre = RangeElement("abc", False)
    assert nre is not None
    assert nre.is_positive_logic == False

    assert nre.is_match("a") == False
    assert nre.is_match("x") == True
