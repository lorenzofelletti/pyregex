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
    assert type(ast.child.children[0]) is Element
