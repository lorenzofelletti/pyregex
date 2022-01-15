import pytest
from ..src.re_ast import RE, EndElement, GroupNode, Element, RangeElement, SpaceElement, StartElement
from ..src.pyrser import Pyrser


@pytest.fixture
def parser():
    return Pyrser()


def test_simple_regex(parser):
    ast = parser.parse('a')
    print(ast)
    assert type(ast) is RE
    assert type(ast.child) is GroupNode
    assert type(ast.child.children[0]) is Element


def test_grouping(parser):
    ast = parser.parse('a(b)c')

    # top level group
    assert len(ast.child.children) == 3
    assert type(ast.child.children[0]) is Element
    assert type(ast.child.children[1]) is GroupNode
    assert type(ast.child.children[2]) is Element

    # ast.child.children[1] group '(a)'
    assert len(ast.child.children[1].children) == 1
    assert type(ast.child.children[1].children[0]) is Element


def test_curly_braces_1(parser):
    ast = parser.parse('a{5}b')
    assert len(ast.child.children) == 2


def test_fail_curly(parser):
    with pytest.raises(Exception):
        parser.parse('a{3,3}}')


def test_fail_no_closing_par(parser):
    with pytest.raises(Exception):
        parser.parse('a[d]((vfw)')


def test_parse_match_start_end(parser):
    ast = parser.parse('^aaaa.*a$')
    assert len(ast.child.children) == 8


def test_complex_regex(parser):
    ast = parser.parse('^[a-z|A-Z]{1,20}@[a-z|A-Z]\.[a-z]{1,3}$')
    assert len(ast.child.children) == 7

    assert type(ast.child.children[0]) is StartElement

    assert type(ast.child.children[1]) is RangeElement
    assert ast.child.children[1].min == 1
    assert ast.child.children[1].max == 20

    assert type(ast.child.children[2]) is Element

    assert type(ast.child.children[3]) is RangeElement

    assert type(ast.child.children[4]) is Element

    assert type(ast.child.children[5]) is RangeElement
    assert ast.child.children[5].min == 1
    assert ast.child.children[5].max == 3

    assert type(ast.child.children[6]) is EndElement


def test_space_element(parser):
    ast = parser.parse('\s')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is SpaceElement
