import pytest
from ..src.engine import RegexEngine


@pytest.fixture
def reng():
    return RegexEngine()


def test_simplest(reng):
    assert (True, 1) == reng.match('a', 'a')


def test_simplest_with_wildcard(reng):
    assert (True, 1) == reng.match('.', 'a')


def test_simplest_but_longer(reng):
    assert (True, 3) == reng.match('a.c', 'abc')


def test_wildcard(reng):
    assert (True, 2) == reng.match('.*a', 'aa')


def test_backtracking(reng):
    assert (True, 4) == reng.match('a*a', 'aaaa')


def test_or(reng):
    assert (True, 1) == reng.match('a.*|b', 'b')


def test_or_no_match(reng):
    res, consumed = reng.match('^a|b$', 'c')
    assert res == False


def test_or_no_match_with_bt(reng):
    res, consumed = reng.match('a|b', 'c')
    assert res == False


def test_bt_no_match(reng):
    res, consumed = reng.match('a{5}a', 'aaaaa')
    assert res == False


def test_match_group_zero_or_more(reng):
    res, consumed = reng.match('(a)*', 'aa')
    assert (True, 2) == (res, consumed)


def test_fail_group_one_or_more(reng):
    res, cons = reng.match('^(a)+', 'b')
    assert res == False


def test_complex_match(reng):
    res, cons = reng.match('^(a|b+c)?[n-z]{2}', 'axx')
    assert res == True


def test_complex_match_2(reng):
    res, cons = reng.match('^(a|b+c)?[n-z]{2}', 'xx')
    assert res == True


def test_match_mail_simple(reng):
    res, cons = reng.match(r'.*@.*\.(com|it)', 'vr@gmail.com')
    assert res == True


def test_bt_index_leaf(reng):
    res, cons = reng.match(r'^aaaa.*a$', 'aaaaa')
    assert res == True


def test_bt_index_or(reng):
    res, cons = reng.match(r'^x(a|b)?bc$', 'xbc')
    assert res == True


def test_bt_index_group(reng):
    res, cons = reng.match(r'^x(a)?ac$', 'xac')
    assert res == True


def test_match_or_left(reng):
    res, cons = reng.match('na|nb', 'na')
    assert res == True


def test_match_or_right(reng):
    res, cons = reng.match('na|nb', 'nb')
    assert res == True


def test_match_or_right_at_start_end(reng):
    res, cons = reng.match('^na|nb$', 'nb')
    assert res == True


def test_no_match_after_end(reng):
    res, cons = reng.match('^na|nb$', 'nb ')
    assert res == False


def test_match_sequence_with_start_end_correctly(reng):
    res, cons = reng.match('^a|b$', 'a  ')
    assert res == True

    res, cons = reng.match('^a|b$', ' a  ')
    assert res == False

    res, cons = reng.match('^a|b$', '  b')
    assert res == True

    res, cons = reng.match('^a|b$', '  b ')
    assert res == False


def test_complex_match_3(reng):
    res, _ = reng.match('a(b|[c-n])+b{3}.{2}', 'ahhbbbbbb')
    assert res == True


def test_bit_less_complex_match_3(reng):
    res, _ = reng.match('a(b|[c-n])+b{3}', 'ahhbbbbbb')
    assert res == True


def test_unescaped_special_ch(reng):
    with pytest.raises(Exception):
        reng.match('$a^', 'aa')


def test_various_emails(reng):
    res, _ = reng.match('.*@(gmail|hotmail).(com|it)', 'baa.aa@hotmail.it')
    assert res == True
    res, _ = reng.match('.*@(gmail|hotmail).(com|it)', 'baa.aa@gmail.com')
    assert res == True
    res, _ = reng.match('.*@(gmail|hotmail).(com|it)', 'baa.aa@hotmaila.com')
    assert res == False


def test_match_empty(reng):
    res, _ = reng.match('^$', '')
    assert res == True
    res, _ = reng.match('$', '')
    assert res == True
    res, _ = reng.match('^', '')
    assert res == True


def test_match_space(reng):
    res, _ = reng.match(r'\s', r' ')
    assert res == True
    res, _ = reng.match(r'\s', '\t')
    assert res == True
    res, _ = reng.match(r'\s', '\r')
    assert res == True
    res, _ = reng.match(r'\s', '\f')
    assert res == True
    res, _ = reng.match(r'\s', '\n')
    assert res == True
    res, _ = reng.match(r'\s', '\v')
    assert res == True


def test_match_space_2(reng):
    res, _ = reng.match(r'\s+', '\r\t\n \f \v')
    assert res == True
    res, _ = reng.match(r'^\s$', '\r\t')
    assert res == False


def test_return_matches_simple(reng):
    res, _, matches = reng.match(r'a\s', r'a ', return_matches=True)
    assert res == True
    assert len(matches[0]) == 1


def test_return_matches_two(reng):
    res, _m, matches = reng.match(r'a(b)+a', r'abba', return_matches=True)
    assert res == True
    assert len(matches[0]) == 2


def test_non_capturing_group(reng):
    res, _, matches = reng.match(r'a(?:b)+a', r'abba', return_matches=True)
    assert res == True
    assert len(matches[0]) == 1


def test_continue_after_match_and_return_matches_simple(reng):
    string = 'abba'
    res, consumed, matches = reng.match(
        r'a', string, continue_after_match=True, return_matches=True)
    assert consumed == len(string)
    assert len(matches) == 2
    assert len(matches[0]) == 1
    x = matches[0]
    assert matches[0][0].match == 'a'
    assert len(matches[1]) == 1
    assert matches[1][0].match == 'a'


def test_continue_after_match_and_return_matches_2(reng):
    string = 'abbai'
    res, consumed, matches = reng.match(
        r'a', string, continue_after_match=True, return_matches=True)
    assert consumed == len(string)-1
    assert len(matches) == 2
    assert len(matches[0]) == 1
    x = matches[0]
    assert matches[0][0].match == 'a'
    assert len(matches[1]) == 1
    assert matches[1][0].match == 'a'


def test_question_mark(reng):
    res, _ = reng.match(r'https?://', r'http://')
    assert res == True
    res, _ = reng.match(r'https?://', r'https://')
    assert res == True


def test_engine_1(reng):
    with pytest.raises(Exception):
        res, _ = reng.match("$^", '')


def test_engine_2(reng):
    mail = "lorenzo.felletti@mail.com"
    res, consumed = reng.match(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", mail)
    assert res == True
    assert consumed == len(mail)

    mail = "lorenzo.felletti@mail.c"
    res, _ = reng.match(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", mail)
    assert res == False

    mail = "lorenzo.fellettimail.com"
    res, _ = reng.match(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", mail)
    assert res == False


def test_engine_3(reng):
    string = "lorem ipsum"
    res, consumed = reng.match(r"m", string, continue_after_match=True)
    assert res == True
    assert consumed == len(string)


def test_engine_4(reng):
    string = "lorem ipsum"
    res, consumed, matches = reng.match(
        r"m", string, continue_after_match=True, return_matches=True)
    assert res == True
    assert consumed == len(string)

    assert len(matches) == 2
    assert matches[0][0].match == 'm'
    assert matches[1][0].match == 'm'


def test_engine_5(reng):
    match_1 = "lor.fel@ah.ha"
    match_2 = "fel.log@ha.ah"
    string = match_1 + " " + match_2
    res, consumed, matches = reng.match(
        r"[a-z.]+@[a-z]+\.[a-z]{2}", string, continue_after_match=True, return_matches=True)
    assert res == True
    assert consumed == len(string)

    assert len(matches) == 2
    assert matches[0][0].match == match_1
    assert matches[1][0].match == match_2


def test_engine_6(reng):
    res, consumed = reng.match(r'[\abc]', r'\\')
    assert res == False
    assert consumed == 0

    res, _ = reng.match(r'[\\abc]', r'\\')
    assert res == True


def test_engine_7(reng):
    res, _ = reng.match(r'(a)+(a)?(a{2}|b)+', 'aaabbaa')
    assert res == True


def test_engine_8(reng):
    res, _ = reng.match(r'(a){2}', r'a')
    assert res == False

    res, _ = reng.match(r'(aa){1,2}', r'aa')
    assert res == True


def test_named_group(reng):
    res, _, matches = reng.match(
        r'(?<fancy>clancy)', r'clancy', return_matches=True)
    assert res == True
    assert matches[0][1].name == 'fancy'


def test_named_group_fail_1(reng):
    with pytest.raises(Exception):
        res, _ = reng.match(r"(?<)", '')


def test_named_group_fail_2(reng):
    with pytest.raises(Exception):
        res, _ = reng.match(r"(?<abb)", '')


def test_named_group_fail_empty_name(reng):
    with pytest.raises(Exception):
        res, _ = reng.match(r"(?<>asf)", '')


def test_matches_indexes(reng: RegexEngine):
    test_str = "abbabbab"
    res, consumed, matches = reng.match(
        r"a", test_str, continue_after_match=True, return_matches=True)
    assert res == True
    assert consumed == len(test_str) - 1
    assert len(matches) == 3
    assert matches[0][0].start_idx == 0 and matches[0][0].end_idx == 1
    assert matches[1][0].start_idx == 3 and matches[1][0].end_idx == 4
    assert matches[2][0].start_idx == 6 and matches[2][0].end_idx == 7


def test_returned_matches_indexes(reng: RegexEngine):
    regex = r"(a)(a)(a)(a)(a)(a)"
    test_str = "aaaaaaaaaacccaaaaaac"
    res, consumed, matches = reng.match(regex, test_str, True, True)

    assert res == True
    assert consumed == len(test_str)-1
    assert matches is not None and len(matches) == 2
    assert len(matches[0]) == 7
    assert len(matches[1]) == 7
    assert matches[0][0].start_idx == 0 and matches[0][0].end_idx == 6
    assert matches[0][1].start_idx == 5 and matches[0][1].end_idx == 6
    assert matches[0][2].start_idx == 4 and matches[0][2].end_idx == 5
    assert matches[0][3].start_idx == 3 and matches[0][3].end_idx == 4
    assert matches[0][4].start_idx == 2 and matches[0][4].end_idx == 3
    assert matches[0][5].start_idx == 1 and matches[0][5].end_idx == 2
    assert matches[0][6].start_idx == 0 and matches[0][6].end_idx == 1

    assert matches[1][0].start_idx == 13 and matches[1][0].end_idx == 19
    assert matches[1][1].start_idx == 18 and matches[1][1].end_idx == 19
    assert matches[1][2].start_idx == 17 and matches[1][2].end_idx == 18
    assert matches[1][3].start_idx == 16 and matches[1][3].end_idx == 17
    assert matches[1][4].start_idx == 15 and matches[1][4].end_idx == 16
    assert matches[1][5].start_idx == 14 and matches[1][5].end_idx == 15
    assert matches[1][6].start_idx == 13 and matches[1][6].end_idx == 14
