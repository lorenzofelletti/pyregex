"""Module containing the RegexEngine class.

The RegexEngine class implements a regular expressions engine.

Example:
    Matching a regex with some test string::

        reng = RegexEngine()
        result, consumed = reng.match(r"a+bx", "aabx")
"""


from collections import deque
from typing import Callable, Deque, Union, Tuple, List
import unicodedata
from .pyrser import Pyrser
from .match import Match
from .re_ast import RE, GroupNode, LeafNode, OrNode, EndElement, StartElement


class RegexEngine:
    """ Regular Expressions Engine.

    This class contains all the necessary to recognize regular expressions in a test string.
    """

    def __init__(self):
        self.parser: Pyrser = Pyrser()
        self.prev_re: str = None
        self.prev_ast: RE = None

    def match(self, re: str, string: str, return_matches: bool = False, continue_after_match: bool = False, ignore_case: int = 0) -> Union[Tuple[bool, int, List[Deque[Match]]], Tuple[bool, int]]:
        """ Searches a regex in a test string.

        Searches the passed regular expression in the passed test string and
        returns the result.

        It is possible to customize both the returned value and the search
        method.

        The ignore_case flag may cause unexpected results in the returned
        number of matched characters, and also in the returned matches, e.g.
        when the character ẞ is present in either the regex or the test string.

        Args:
            re (str): the regular expression to search
            string (str): the test string
            return_matches (bool): if True a data structure containing the
                matches - the whole match and the subgroups matched
                (default is False)
            continue_after_match (bool): if True the engine continues
                matching until the whole input is consumed
                (default is False)
            ignore_case (int): when 0 the case is not ignored, when 1 a "soft"
                case ignoring is performed, when 2 casefolding is performed.
                (default is 0)

        Returns:
            A tuple containing whether a match was found or not, the last
            matched character index, and, if return_matches is True, a
            list of deques of Match, where each list of matches represents
            in the first position the whole match, and in the subsequent
            positions all the group and subgroups matched. 
        """

        def return_fnc(res: bool, consumed: int, all_matches: List[Deque[Match]], return_matches: bool) -> Union[Tuple[bool, int, List[Deque[Match]]], Tuple[bool, int]]:
            """ Create the Tuple to return."""
            if return_matches:
                return res, consumed, all_matches
            else:
                return res, consumed

        if ignore_case == 1:
            re = unicodedata.normalize("NFKD", re).lower()
            string = unicodedata.normalize("NFKD", string).casefold()
        elif ignore_case == 2:
            re = unicodedata.normalize("NFKD", re).casefold()
            string = unicodedata.normalize("NFKD", string).casefold()

        ast = self.parser.parse(re=re) if self.prev_re != re else self.prev_ast
        self.prev_re = re
        self.prev_ast = ast

        # variables holding the matched groups list for each matched substring in the test string
        all_matches: List[Deque[Match]] = []
        highest_matched_idx: int = 0  # holds the highest matched string's index

        res, consumed, matches = self.__match__(ast, string, 0)
        if res:
            highest_matched_idx = consumed
            all_matches.append(matches)
        else:
            return return_fnc(res, highest_matched_idx, all_matches, return_matches)

        if not continue_after_match or not consumed > 0:
            return return_fnc(res, highest_matched_idx, all_matches, return_matches)

        while True:
            res, consumed, matches = self.__match__(ast, string, consumed)

            # if consumed is not grater than highest_matched_idx this means the new match
            # consumed 0 characters, so there is really nothing more to match
            if res and consumed > highest_matched_idx:
                highest_matched_idx = consumed
                all_matches.append(matches)
            else:
                return return_fnc(True, highest_matched_idx, all_matches, return_matches)

    def __match__(self, ast: RE, string: str, start_str_i: int) -> Tuple[bool, int, Deque[Match]]:
        """ Same as match, but always returns after the first match."""
        matches: Deque[Match] = deque()

        # used to restore the left match of a ornode if necessary
        last_match: Match = None

        # str_i represents the matched characters so far. It is inizialized to
        # the value of the input parameter start_str_i because the match could
        # be to be searched starting at an index different from 0, e.g. in the
        # case this function is called to search a second match in the test
        # string.
        str_i = start_str_i

        # max_matched_idx represents the "upper limit" of the match.
        # It is necessary when backtracking in the presence of nested
        # quantifiers, because we need a way to "tell" the group that
        # is causing the fail by being too greedy to stop earlier if
        # possible.
        max_matched_idx = -1

        def return_fnc(res: bool, str_i: int) -> Tuple[bool, int, Deque[Match]]:
            """ Returns the Tuple to be returned by __match__."""
            nonlocal matches
            return res, str_i, matches

        def save_matches(match_group: Callable, ast: Union[RE, GroupNode], string: str, start_idx: int, max_matched_idx=-1) -> Tuple[bool, int]:
            """ Save the matches of capturing groups.

            Args:
                match_group (Callable): the function to use to match the group
                ast (Union[RE, GroupNode]): the group to match
                string (str): the string to match
                start_idx (int): the starting index

            Returns:
                A tuple of the boolean result of the match, and the last matched
                index.
            """
            nonlocal matches
            nonlocal last_match

            res, end_idx = match_group(ast, string, max_matched_idx)

            if ast.is_capturing() and res == True:
                for i in range(0, len(matches)):
                    if matches[i].group_id == ast.group_id:
                        last_match = matches[i]
                        matches.remove(matches[i])
                        break
                matches.appendleft(
                    Match(ast.group_id, start_idx, end_idx, string, ast.group_name))

            return res, end_idx
        
        def remove_leftmost_match():
            """ Used when matching an OrNode.
            
            When matching an OrNode the right children is always saved instead
            of saving the left one when the chosen path goes left. By calling
            this function you remove the leftmost match (the one created by the
            right child).
            """
            nonlocal matches
            matches.popleft()
        
        def appendleft_last_match():
            """ Used when matching an OrNode.
            
            When matching an OrNode the right children is always saved instead
            of saving the left one when the chosen path goes left. By calling
            this function you restore the left match.
            """
            nonlocal matches
            matches.appendleft(last_match)


        def match_group(ast: Union[RE, GroupNode, OrNode], string: str, max_matched_idx: int = -1) -> Tuple[bool, int]:
            """
            Match a group, which is always the case.s

            Returns the match state (True or False) and the new string i, that is the
            number of matched characters in the string so far.
            """
            nonlocal start_str_i
            nonlocal str_i
            backtrack_stack: List[Tuple[int, int, int, List[int]]] = []

            def backtrack(str_i: int, curr_child_i: int, recursive: bool = False) -> Tuple[bool, int, int]:
                """ Returns whether it is possible to backtrack and the state to backtrack to.

                Takes as input the current state of the engine and returns whether
                or not it is possible to backtrack.

                Args:
                    str_i (int): the current considered index of the test string
                    curr_child_i (int): the index of the GroupNode children considered

                Returns:
                    A Tuple containing a bool, True if it is possible to backtrack,
                    the new string index, and the new node children index to which
                    backtrack to. Note that the last two parameters only have a
                    meaning in the case it is possible to backtrack (the bool is
                    True).
                """
                nonlocal backtrack_stack
                nonlocal max_matched_idx
                nonlocal ast

                if len(backtrack_stack) == 0:
                    return False, str_i, curr_child_i

                # the fist step is to pop the last tuple from the backtrack_stack
                popped_child_i, min_, matched_times, consumed_list = backtrack_stack.pop()

                if matched_times == min_:
                    # if a node is already matched the minimum number of times, the
                    # chance you have to potentially be able to backtrack is to is
                    # to delete the entry from the stack and then search for a new
                    # possibility (recursively calling this function).
                    # But, before the recursion, you have to calculate  what the
                    # string index (str_i) value was before the node was matched
                    # even once. Thus, you have to decrease the string index
                    # of each consumption in the consumed_list.

                    # calculate_the new str_i
                    before_str_i = str_i
                    for consumption in consumed_list:
                        str_i -= consumption
                    if max_matched_idx == -1 or isinstance(ast.children[popped_child_i], LeafNode) or before_str_i == str_i:
                        # recursive call
                        return backtrack(str_i, popped_child_i, True)
                    else:
                        # case of backtracking from nested quantifier
                        # returns "not recursive" because if it is the case
                        # of a recursive call, this is outside of the case of
                        # simply nested quantifiers, and in I cannot backtrack
                        # anymore
                        return not recursive, str_i, popped_child_i
                else:
                    # the node was matched more times than its min, so you just
                    # need to remove the last consumption from the list,
                    # decrease the str_i by that amount, decrease the times the node
                    # was matched - matched_times - by 1, and then append the stack
                    # the tuple with the new matched_times and consumed_list.
                    last_consumed = consumed_list.pop()
                    new_str_i = str_i - last_consumed
                    if max_matched_idx == -1 or isinstance(ast.children[popped_child_i], LeafNode):
                        backtrack_stack.append(
                            (popped_child_i, min_, matched_times - 1, consumed_list))
                        # lastly, you return that the backtracking is possible, and
                        # the state to which backtrack to.
                        return True, new_str_i, curr_child_i
                    else:
                        # case of backtracking from nested quantifier
                        return not recursive, new_str_i, popped_child_i

            def remove_this_node_from_stack(curr_child_i: int, str_i: int) -> int:
                """ Removes node from stack and returns the new str_i.
                """
                nonlocal backtrack_stack
                popped_child_i, min_, matched_times, consumed_list = backtrack_stack.pop()
                if popped_child_i == curr_child_i:
                    for consumption in consumed_list:
                        str_i -= consumption
                else:
                    backtrack_stack.append((popped_child_i, min_, matched_times, consumed_list))
                return str_i

            curr_node = ast.children[0] if len(ast.children) > 0 else None
            i = 0  # the children i'm iterating, not to confuse with str_i

            # the passed ast can't be a Leaf
            while i < len(ast.children):
                curr_node = ast.children[i]

                # if is OrNode I evaluate the sub-groups with a recursive call
                if isinstance(curr_node, OrNode):
                    before_str_i = str_i
                    min_, max_ = curr_node.min, curr_node.max
                    j = 0
                    consumed_list = []

                    backtracking = False
                    while j < max_:
                        tmp_str_i = str_i

                        save_match_left = isinstance(curr_node.left, GroupNode)
                        res_left, str_i_left = save_matches(match_group, curr_node.left, string, str_i, max_matched_idx) if save_match_left else match_group(curr_node.left, string, max_matched_idx)

                        str_i = tmp_str_i

                        save_match_right = isinstance(curr_node.right, GroupNode)
                        res_right, str_i_right = save_matches(match_group, curr_node.right, string, str_i, max_matched_idx) if save_match_right else match_group(curr_node.right, string, max_matched_idx)

                        if res_left and res_right:
                            # choose the one that consumed the most character
                            # unless it exceeds the max_matched_idx
                            chose_left = (str_i_left >= str_i_right)
                            str_i = str_i_left if chose_left else str_i_right
                            if max_matched_idx != -1 and str_i > max_matched_idx:
                                # tries to stay below the max_matched_idx threshold
                                str_i = str_i_right if chose_left else str_i_left
                            if chose_left:
                                if save_match_right:
                                    remove_leftmost_match()
                                if save_match_left:
                                    appendleft_last_match()
                            else:
                                # chose right
                                if save_match_left and not save_match_right:
                                    # there is a spurious match originated from
                                    # the left child
                                    remove_leftmost_match()

                        elif res_left and not res_right:
                            str_i = str_i_left
                        elif not res_left and res_right:
                            str_i = str_i_right

                        res = (res_left or res_right)

                        if res == True and (max_matched_idx == -1 or str_i <= max_matched_idx):
                            if (str_i - tmp_str_i == 0) and j >= min_:
                                max_matched_idx = -1
                                break
                            consumed_list.append(str_i - tmp_str_i)
                        else:
                            if min_ <= j:
                                max_matched_idx = -1
                                break
                            if i > 0 and not isinstance(ast.children[i-1], LeafNode):
                                str_i = remove_this_node_from_stack(i, str_i)
                            if str_i == start_str_i:
                                return False, str_i
                            max_matched_idx = str_i - 1 if max_matched_idx == -1 else max_matched_idx - 1
                            can_bt, bt_str_i, bt_i = backtrack(str_i, i)
                            if can_bt:
                                i = bt_i
                                str_i = bt_str_i
                                backtracking = True
                                break  # retry to match the current node
                            else:
                                return False, str_i
                        j += 1
                    if not backtracking:
                        backtrack_stack.append(
                            (i, min_, j, consumed_list))
                        max_matched_idx = -1
                        i += 1
                    continue

                elif isinstance(curr_node, GroupNode):
                    min_, max_ = curr_node.min, curr_node.max
                    j = 0
                    consumed_list = []
                    before_str_i = str_i

                    backtracking = False
                    while j < max_:
                        tmp_str_i = str_i

                        res, new_str_i = save_matches(
                            match_group, curr_node, string, str_i, max_matched_idx)
                        if res == True and (max_matched_idx == -1 or new_str_i <= max_matched_idx):
                            # i must use tmp_str_i because str_i is changed by the match_group
                            # call, so (new_str_i - str_i) would be always 0
                            if (new_str_i - tmp_str_i == 0) and j >= min_:
                                max_matched_idx = -1
                                break
                            consumed_list.append(new_str_i - tmp_str_i)
                            #str_i = new_str_i
                        else:
                            if min_ <= j:
                                # i did the bare minimum or more
                                max_matched_idx = -1
                                break
                            if i > 0 and not isinstance(ast.children[i-1], LeafNode):
                                str_i = remove_this_node_from_stack(i, str_i)
                                if str_i == start_str_i:
                                    return False, str_i
                                max_matched_idx = str_i - 1 if max_matched_idx == -1 else max_matched_idx - 1
                            can_bt, bt_str_i, bt_i = backtrack(str_i, i)
                            if can_bt:
                                i = bt_i
                                str_i = bt_str_i
                                backtracking = True
                                break  # retry to match the current node
                            else:
                                return False, str_i
                        j += 1

                    # if NOT backtracking iterate the next element, and put the
                    # current on the backtrack_stack, otherwise don't increment i, don't put on the
                    # stack so to retry the current one (just continue)
                    if not backtracking:
                        backtrack_stack.append(
                            (i, min_, j, consumed_list))
                        max_matched_idx = -1
                        i += 1

                    continue

                elif isinstance(curr_node, LeafNode):
                    # it is a LeafNode obviously now
                    min_, max_ = curr_node.min, curr_node.max
                    j = 0

                    consumed_list = []

                    before_str_i = str_i  # to discard changes made in case i need to bt

                    backtracking = False
                    while j < max_:
                        if str_i < len(string):  # i still have input to match
                            if curr_node.is_match(ch=string[str_i], str_i=str_i, str_len=len(string)) and (max_matched_idx == -1 or str_i < max_matched_idx):
                                if not (isinstance(curr_node, StartElement) or isinstance(curr_node, EndElement)):
                                    consumed_list.append(1)
                                    str_i += 1
                            else:
                                if min_ <= j:  # I already met the minimum requirement for match
                                    break
                                if i > 0 and not isinstance(ast.children[i-1], LeafNode):
                                    str_i = remove_this_node_from_stack(i, str_i)
                                    if str_i == start_str_i:
                                        return False, str_i
                                    max_matched_idx = str_i - 1
                                can_bt, bt_str_i, bt_i = backtrack(
                                    before_str_i, i)
                                if can_bt:
                                    i = bt_i
                                    str_i = bt_str_i
                                    backtracking = True
                                    break
                                else:
                                    return False, str_i
                        else:  # finished input
                            if isinstance(curr_node, StartElement) or isinstance(curr_node, EndElement) and curr_node.is_match(str_i=str_i, str_len=len(string)):
                                pass
                            # finished input w/o finishing the regex tree
                            elif min_ <= j:
                                break
                            else:
                                # i have more states, but the input is finished
                                can_bt, bt_str_i, bt_i = backtrack(
                                    before_str_i, i)
                                if can_bt:
                                    i = bt_i
                                    str_i = bt_str_i
                                    backtracking = True
                                    break
                                else:
                                    return False, str_i
                        j += 1
                    if not backtracking:
                        backtrack_stack.append(
                            (i, min_, j, consumed_list))
                        i += 1
                    continue
                else:
                    return False, str_i

            return True, str_i

        i = str_i

        if len(string) == 0:
            res, consumed = save_matches(
                match_group=match_group, ast=ast, string=string, start_idx=str_i)
            return return_fnc(res, consumed)

        while str_i < len(string):
            res, _ = save_matches(match_group=match_group,
                                  ast=ast, string=string, start_idx=str_i)
            i += 1
            if res:
                return return_fnc(True, str_i)
            else:
                matches = deque()
                str_i = i
        return return_fnc(False, str_i)
