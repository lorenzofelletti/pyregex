"""Module containing the RegexEngine class.

The RegexEngine class implements a regular expressions engine.

Example:
    Matching a regex with some test string::

        reng = RegexEngine()
        result, consumed = reng.match(r"a+bx", "aabx")
"""


from typing import Callable, Union, Tuple, List
from .pyrser import Pyrser
from .match import Match
from .re_ast import RE, GroupNode, LeafNode, OrNode, EndElement, StartElement


class RegexEngine:
    """ Regular Expressions Engine.

    This class contains all the necessary to recognize regular expressions in a test string.
    """

    def __init__(self):
        self.parser: Pyrser = Pyrser()

    def match(self, re: str, string: str, return_matches: bool = False, continue_after_match: bool = False) -> Union[Tuple[bool, int, List[List[Match]]], Tuple[bool, int]]:
        """ Searches a regex in a test string.

        Searches the passed regular expression in the passed test string and
        returns the result.

        It is possible to customize both the returned value and the search
        method.

        Args:
            re (str): the regular expression to search
            string (str): the test string
            return_matches (bool): if True a data structure containing the
                matches - the whole match and the subgroups matched
                (default is False)
            continue_after_match (bool): if True the engine continues
                matching until the whole input is consumed
                (default is False)

        Returns:
            A tuple containing whether a match was found or not, the last
            matched character index, and (if return_matches is True) a
            list of lists of Match, where each list of matches represents
            in the first position the whole match, and in the subsequent
            positions all the group and subgroups matched. 
        """

        def return_fnc(res: bool, str_i: int, all_matches: list, return_matches: bool) -> Union[Tuple[bool, int, List[List[Match]]], Tuple[bool, int]]:
            """ If return_matches is True returns the matches."""
            if return_matches:
                return res, str_i, all_matches
            else:
                return res, str_i

        all_matches = []  # variables holding the matched groups list for each matched substring in the test string
        highest_matched_idx = 0  # holds the highest test_str index matched

        res, str_i, matches = self.__match__(re, string, 0)
        if res:
            highest_matched_idx = str_i
            all_matches.append(matches)
        else:
            return return_fnc(res, highest_matched_idx, all_matches, return_matches)

        if not continue_after_match:
            return return_fnc(res, highest_matched_idx, all_matches, return_matches)

        while True:
            #string = string[str_i:]
            if not len(string) > 0:
                return return_fnc(res, highest_matched_idx, all_matches, return_matches)
            res, str_i, matches = self.__match__(re, string, str_i)
            if res:
                highest_matched_idx = str_i
                all_matches.append(matches)
            else:
                return return_fnc(True, highest_matched_idx, all_matches, return_matches)

    def __match__(self, re: str, string: str, start_str_i: int) -> Tuple[bool, int, List[Match]]:
        """ Same as match, but always returns after the first match."""
        ast = self.parser.parse(re=re)
        matches: List[Match]
        matches = []

        # str_i represents the matched characters so far. It is inizialized to
        # the value of the input parameter start_str_i because the match could
        # be to be searched starting at an index different from 0, e.g. in the
        # case this function is called to search a second match in the test
        # string.
        str_i = start_str_i

        def return_fnc(res: bool, str_i: int) -> Tuple[bool, int, List[Match]]:
            """ Returns the Tuple to be returned by __match__."""
            nonlocal matches
            # reverses the list so the last match (the "whole" match) is first
            matches.reverse()
            return res, str_i, matches

        def backtrack(backtrack_stack: List[Tuple[int, int, int, List[int]]], str_i: int, curr_i: int) -> Tuple[bool, int, int]:
            """ Returns whether it is possible to backtrack and the state to backtrack to.

            Takes as input the current state of the engine and returns whether
            or not it is possible to backtrack.

            Args:
                backtrack_stack (List[Tuple[int, int, int, List[int]]]): the
                current backtrack_stack situation. The Tuple values represents,
                in order from left to right, the node index of the entry in its
                parent children list, the minimum times that node must be
                matched, the time it is matched in the current state, the list
                of consumed character each times it was matched
                str_i (int): the current considered index of the test string
                curr_i (int): the index of the GroupNode children considered

            Returns:
                A Tuple containing a bool, True if it is possible to backtrack,
                the new string index, and the new node children index to which
                backtrack to. Note that the last two parameters only have a
                meaning in the case it is possible to backtrack (the bool is
                True).
            """
            if len(backtrack_stack) == 0:
                return False, str_i, curr_i

            # the fist step is to pop the last tuple from the backtrack_stack
            node_i, min_, matched_times, consumed_list = backtrack_stack.pop()

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
                for consumption in consumed_list:
                    str_i -= consumption
                # recursive call
                return backtrack(backtrack_stack, str_i, node_i)
            else:
                # the node was matched more times than its min, so you just
                # need to remove the last consumption from the list,
                # decrease the str_i by that amount, decrease the times the node
                # was matched - matched_times - by 1, and then append the stack
                # the tuple with the new matched_times and consumed_list.
                last_consumed = consumed_list.pop()
                new_str_i = str_i - last_consumed
                backtrack_stack.append(
                    (node_i, min_, matched_times - 1, consumed_list))
                # lastly, you return that the backtracking is possible, and
                # the state to which backtrack to.
                return True, new_str_i, curr_i

        def save_matches(match_group: Callable, ast: Union[RE, GroupNode], string: str, start_idx: int) -> Tuple[bool, int]:
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

            res, end_idx = match_group(ast, string)

            if ast.is_capturing() and res == True:
                for i in range(0, len(matches)):
                    if matches[i].group_id == ast.group_id:
                        matches.remove(matches[i])
                        break
                matches.append(
                    Match(ast.group_id, start_idx, end_idx, string, ast.group_name))

            return res, end_idx

        def match_group(ast: Union[RE, GroupNode, OrNode], string: str) -> Tuple[bool, int]:
            '''
            Match a group, which is always the case.s

            Returns the match state (True or False) and the new string i, that is the
            number of matched characters in the string so far.
            '''
            nonlocal str_i
            backtrack_stack = []
            curr_node = ast.children[0]
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
                        res, new_str_i = match_group(ast=curr_node.left, string=string) if not isinstance(
                            curr_node.left, GroupNode) else save_matches(match_group=match_group, ast=curr_node.left, string=string, start_idx=str_i)
                        if res == True:
                            pass
                        else:
                            str_i = tmp_str_i
                            res, new_str_i = match_group(ast=curr_node.right, string=string) if not isinstance(
                                curr_node.right, GroupNode) else save_matches(match_group=match_group, ast=curr_node.right, string=string, start_idx=str_i)

                        if res == True:
                            consumed_list.append(new_str_i - tmp_str_i)
                        elif min_ <= j:
                            break
                        else:
                            can_bt, bt_str_i, bt_i = backtrack(
                                backtrack_stack, str_i, i)
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
                            match_group, curr_node, string, str_i)
                        if res == True:
                            # i must use tmp_str_i because str_i is changed by the match_group
                            # call, so (new_str_i - str_i) would be always 0
                            consumed_list.append(new_str_i - tmp_str_i)
                            #str_i = new_str_i
                        elif min_ <= j:
                            # i did the bare minimum or more
                            break
                        else:
                            can_bt, bt_str_i, bt_i = backtrack(
                                backtrack_stack, str_i, i)
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
                            if curr_node.is_match(ch=string[str_i], str_i=str_i, str_len=len(string)):
                                if not (isinstance(curr_node, StartElement) or isinstance(curr_node, EndElement)):
                                    consumed_list.append(1)
                                    str_i += 1
                            else:
                                if min_ <= j:  # I already met the minimum requirement for match
                                    break
                                can_bt, bt_str_i, bt_i = backtrack(
                                    backtrack_stack, before_str_i, i)
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
                                    backtrack_stack, before_str_i, i)
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
                matches = []
                str_i = i
        return return_fnc(False, str_i)
