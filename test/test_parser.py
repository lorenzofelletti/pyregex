import pytest
from ..src.re_ast import RE, GroupNode, Element
from ..src.pyrser import Pyrser


@pytest.fixture
def parser():
    return Pyrser()


def test_simple_regex(parser):
    ast = parser.parse('a')
    print(ast)
    assert type(ast) is RE
    assert ast.match_start == False
    assert ast.match_end == False
    assert type(ast.child) is GroupNode
    assert type(ast.child.children[1]) is Element


def test_grouping(parser):
    ast = parser.parse('a(b)c')

    # top level group
    assert len(ast.child.children) == 5
    assert type(ast.child.children[0+1]) is Element
    assert type(ast.child.children[1+1]) is GroupNode
    assert type(ast.child.children[2+1]) is Element

    # ast.child.children[1] group '(a)'
    assert len(ast.child.children[1+1].children) == 1
    assert type(ast.child.children[1+1].children[0]) is Element


def test_curly_braces_1(parser):
    ast = parser.parse('a{5}b')
    assert len(ast.child.children) == 2+2
