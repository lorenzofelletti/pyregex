import numpy as np
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
    ast = parser.parse(r'a{5}b')
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
    ast = parser.parse(r'^[a-zA-Z]{1,20}@[a-zA-Z]\.[a-z]{1,3}$')
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
    ast = parser.parse(r'\s')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is SpaceElement


def test_range_1(parser):
    ast = parser.parse('[^a-z]')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is RangeElement
    assert ast.child.children[0].is_match('a') == False


def test_range_2(parser):
    ast = parser.parse(r'[^a-z-\s-]')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is RangeElement
    assert ast.child.children[0].is_match('a') == False
    assert ast.child.children[0].is_match('-') == False
    ast.child.children[0].is_match(' ') == False


def test_range_3(parser):
    ast = parser.parse(r'[a-z-\s-]')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is RangeElement
    assert ast.child.children[0].is_match('a') == True
    assert ast.child.children[0].is_match('-') == True
    ast.child.children[0].is_match(' ') == True


def test_range_2(parser):
    ast = parser.parse(r'[\]]')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is RangeElement
    assert ast.child.children[0].is_match(']') == True


def test_parse_curly_1(parser):
    ast = parser.parse(r'a{2}')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is Element
    assert ast.child.children[0].is_match('a') == True
    assert ast.child.children[0].min == 2
    ast.child.children[0].max == 2


def test_parse_curly_2(parser):
    ast = parser.parse(r'a{,2}')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is Element
    assert ast.child.children[0].is_match('a') == True
    assert ast.child.children[0].min == 0
    ast.child.children[0].max == 2


def test_parse_curly_3(parser):
    ast = parser.parse(r'a{2,}')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is Element
    assert ast.child.children[0].is_match('a') == True
    assert ast.child.children[0].min == 2
    ast.child.children[0].max == np.inf


def test_parse_curly_4(parser):
    ast = parser.parse(r'a{,}')
    assert len(ast.child.children) == 1
    assert type(ast.child.children[0]) is Element
    assert ast.child.children[0].is_match('a') == True
    assert ast.child.children[0].min == 0
    ast.child.children[0].max == np.inf


def test_parse_fail_empty_curly(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'a{}')


def test_fail_quatifier_unescaped(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'?')


def test_parse_fail_missing_clising_bracket(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'a[abc')


def test_parse_fail_unescaped_closing_bracket(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'abc]')


def test_parse_fail_unescaped_closing_parenthesis(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'a)')


def test_parse_fail_unescaped_start(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'^^')


def test_parse_fail_unescaped_end(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'$$')


def test_parse_fail_swapped_range(parser):
    with pytest.raises(Exception):
        ast = parser.parse(r'[z-a]')


def test_parse_fail_non_capturing_group(parser):
    with pytest.raises(Exception):
        parser.parse(r'(?')

    with pytest.raises(Exception):
        parser.parse(r'(?aa')


def test_parse_fail_non_closed_range(parser):
    with pytest.raises(Exception):
        parser.parse(r'[a')

    with pytest.raises(Exception):
        parser.parse(r'[')
