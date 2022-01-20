import pytest
from ..src.re_ast import ASTNode, RE, LeafNode, Element, WildcardElement, SpaceElement, RangeElement, StartElement, EndElement, OrNode, NotNode, GroupNode


def test_ASTNode():
    ast_node = ASTNode()
    assert ast_node is not None


def test_RE():
    re = RE(child=Element(match_ch='e'))
    assert re is not None

    assert hasattr(re, 'type')
    assert hasattr(re, 'child')
    assert hasattr(re, 'children')

    assert re.type == 're'
    assert re.child is re.children[0]


def test_NotNode():
    not_node = NotNode(child=Element(match_ch='e'))
    assert not_node is not None

    assert hasattr(not_node, 'type')
    assert hasattr(not_node, 'child')
    assert hasattr(not_node, 'children')

    assert not_node.type == 'notNode'
    assert not_node.child is not_node.children[0]
