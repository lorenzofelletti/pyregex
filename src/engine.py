from pydoc import doc
from typing import Callable

from numpy import append
from .pyrser import Pyrser
from .match import Match
from .re_ast import ASTNode, Element, GroupNode, LeafNode, NotNode, OrNode, RangeElement, RE, WildcardElement, EndElement, StartElement


class RegexEngine:
    def __init__(self):
        self.parser = Pyrser()

    def match(self, re: str, string: str, return_matches=False, continue_after_match=False):
        def return_fnc(res: bool, str_i: int, all_matches: list, return_matches: bool):
            if return_matches:
                return res, str_i, all_matches
            else:
                return res, str_i

        all_matches = []

        res, str_i, matches = self.__match__(re, string, True)
        if res:
            all_matches.append(matches)

        if not continue_after_match:
            return return_fnc(res, str_i, all_matches, return_matches)

        while True:
            string = string[str_i:]
            if not len(string) > 0:
                return return_fnc(res, str_i, all_matches, return_matches)
            res, str_i, matches = self.__match__(re, string, True)
            if res:
                all_matches.append(matches)

    def __match__(self, re: str, string: str, return_matches=False):
        """
        Same as match, but always returns after the first match.
        """
        ast = self.parser.parse(re=re)
        matches = []

        str_i = 0  # matched string chars so far

        def return_fnc(res: bool, str_i: int):
            nonlocal return_matches, matches
            if return_matches:
                return res, str_i, matches
            else:
                return res, str_i

        def backtrack(backtrack_stack: list, str_i, curr_i):
            '''
            Retun a tuple: 
             - bool: can/can't I backtrack
             - new_str_i: the new str_i to use
            '''
            if len(backtrack_stack) == 0:
                return False, str_i, curr_i

            node_i, min_, matched_times, consumed_list = backtrack_stack.pop()

            if node_i is None:
                # the backtrack_stack is empty
                return False, str_i, curr_i
            elif matched_times == min_:
                # calculate_the new correct str_i
                for consumption in consumed_list:
                    str_i -= consumption
                # recursive call
                return backtrack(backtrack_stack, str_i, node_i)
            else:
                if len(consumed_list) == 0:
                    return False, str_i, curr_i

                else:
                    last_consumed = consumed_list.pop()
                    new_str_i = str_i - last_consumed
                    backtrack_stack.append(
                        (node_i, min_, matched_times - 1, consumed_list))
                    return True, new_str_i, curr_i

        def save_matches(match_group: Callable, ast: ASTNode, string: str, start_idx: int):
            nonlocal matches

            res, end_idx = match_group(ast, string)

            if ast.is_capturing() and res == True:
                already_matched = False
                for match in matches:
                    if match.group_id == ast.id:
                        match = Match(ast.id, start_idx, end_idx, string)
                        already_matched = True
                        break
                if not already_matched:
                    matches.append(Match(ast.id, start_idx, end_idx, string))

            return res, end_idx

        def match_group(ast: ASTNode, string: str):
            '''
            Match a group, which is always the case.

            Use recursion when it meets a OrNode.

            Returns the match state (True or False) and the new string i, that is the
            number of matched characters in the string so far.
            '''
            nonlocal str_i
            backtrack_stack = []
            # curr_tkn here is always a group or ornode
            # because recursion occur only w/ OrNode,
            # which
            curr_tkn = ast.children[0]
            i = 0  # the children i'm iterating, not to confuse with str_i

            # the passed ast can't be a Leaf
            while i < len(ast.children):
                curr_tkn = ast.children[i]

                # if is OrNode I evaluate the sub-groups with a recursive call
                if isinstance(curr_tkn, OrNode):
                    before_str_i = str_i
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    j = 0
                    consumed_list = []

                    backtracking = False
                    while j < max_:
                        tmp_str_i = str_i
                        res, new_str_i = match_group(
                            ast=curr_tkn.left, string=string)
                        if res == True:
                            pass
                        else:
                            str_i = tmp_str_i
                            res, new_str_i = match_group(
                                ast=curr_tkn.right, string=string)

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

                elif isinstance(curr_tkn, GroupNode):
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    j = 0
                    consumed_list = []
                    before_str_i = str_i

                    backtracking = False
                    while j < max_:
                        tmp_str_i = str_i

                        # res, new_str_i = match_group(
                        #    ast=curr_tkn, string=string)
                        res, new_str_i = save_matches(
                            match_group, curr_tkn, string, str_i)
                        if res == True:
                            # yes! Come on!
                            # i must use the before_str_i because str_i is changed by the match_group
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

                elif type(curr_tkn) is StartElement or type(curr_tkn) is EndElement:
                    if type(curr_tkn) is StartElement and str_i == 0:
                        i += 1
                    elif type(curr_tkn) is EndElement and str_i == len(string):
                        i += 1
                    else:
                        can_bt, bt_str_i, bt_i = backtrack(
                            backtrack_stack, str_i, i)
                        if can_bt:
                            i = bt_i
                            str_i = bt_str_i
                        else:
                            return False, str_i
                    continue

                elif isinstance(curr_tkn, LeafNode):
                    # it is a LeafNode obviously now
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    j = 0

                    consumed_list = []

                    before_str_i = str_i  # to discard changes made in case i need to bt

                    backtracking = False
                    while j < max_:
                        if str_i < len(string):  # i still have input to match
                            if curr_tkn.is_match(ch=string[str_i]):
                                consumed_list.append(1)
                                str_i += 1
                            else:
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
                            # finished input w/o finishing the regex tree
                            if min_ <= j:
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

        i = 0
        _ = 0

        if len(string) == 0:
            res, consumed = save_matches(
                match_group=match_group, ast=ast, string=string, start_idx=0)
            return return_fnc(res, consumed)

        while str_i < len(string):
            res, _ = save_matches(match_group=match_group,
                                  ast=ast, string=string, start_idx=str_i)
            i += 1
            if res:
                matches.reverse()
                return return_fnc(True, str_i)
            else:
                str_i = i
        return return_fnc(False, _)
