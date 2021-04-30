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


def test_fail_curly(parser):
    with pytest.raises(Exception):
        parser.parse('a{3,3}}')


def test_fail_no_closing_par(parser):
    with pytest.raises(Exception):
        parser.parse('a[d]((vfw)')


def test_parse_match_start_end(parser):
    ast = parser.parse('^aaaa.*a$')
    assert len(ast.child.children) == 6
