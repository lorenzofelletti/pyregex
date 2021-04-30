import numpy as np
import copy
from .pyrser import Pyrser
from .re_ast import ASTNode, Element, GroupNode, LeafNode, NotNode, OrNode, RangeElement, RE, WildcardElement


class RegexEngine:
    def __init__(self):
        self.parser = Pyrser()

    def match(self, re: str, string: str):
        ast = self.parser.parse(re=re)
        prev_node = None
        curr_tkn = ast
        str_i = 0  # matched string chars so far

        def backtrack(backtrack_stack: list, str_i):
            '''
            Retun a tuple: 
             - bool: can/can't I backtrack
             - new_str_i: the new str_i to use
            '''
            if len(backtrack_stack) == 0:
                return False, str_i
            node, min_, matched_times, consumed_list = backtrack_stack.pop()

            if node is None:
                return False, str_i
            elif matched_times == min_:
                if min_ != 0:
                    return False, str_i
                else:
                    # min for the popped element is 0 so i can try popping another (recursive call)
                    return backtrack(backtrack_stack, str_i)
            else:
                last_consumed = consumed_list.pop()
                new_str_i = str_i - last_consumed
                backtrack_stack.append(
                    (node, min_, matched_times - 1, consumed_list))
                return True, new_str_i

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
                        #before_backtrack_stack = copy.deepcopy(backtrack_stack)
                        res, new_str_i = match_group(
                            ast=curr_tkn.left, string=string)
                        if res == True:
                            pass
                        else:
                            str_i = tmp_str_i
                            res, new_str_i = match_group(
                                ast=curr_tkn.right, string=string)

                        if res == True:
                            before_str_i
                            consumed_list.append(new_str_i - tmp_str_i)
                        elif min_ <= j:
                            break
                        else:
                            can_bt, bt_str_i = backtrack(
                                backtrack_stack, str_i)
                            if can_bt:
                                str_i = bt_str_i
                                backtracking = True
                                break  # retry to match the current node
                            else:
                                return False, str_i
                        j += 1
                    if not backtracking:
                        backtrack_stack.append(
                            (curr_tkn, min_, j, consumed_list))
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

                        res, new_str_i = match_group(
                            ast=curr_tkn, string=string)
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
                            can_bt, bt_str_i = backtrack(
                                backtrack_stack, str_i)
                            if can_bt:
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
                            (curr_tkn, min_, j, consumed_list))
                        i += 1

                    continue

                elif isinstance(curr_tkn, LeafNode):
                    # it is a LeafNode obviously now
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    match_str = curr_tkn.match if not type(
                        curr_tkn) is WildcardElement else True
                    j = 0

                    consumed_list = []

                    before_str_i = str_i  # to discard changes made in case i need to bt

                    backtracking = False
                    while j < max_:
                        if str_i < len(string):  # i still have input to match
                            if type(match_str) is bool:
                                # i have a wildcard, that match anything but newline
                                if "\n".find(string[str_i]) == -1:
                                    consumed_list.append(1)
                                    str_i += 1
                                elif min_ <= j:
                                    break
                                else:
                                    can_bt, bt_str_i = backtrack(
                                        backtrack_stack, before_str_i)
                                    if can_bt:
                                        str_i = bt_str_i
                                        backtracking = True
                                        break
                                    else:
                                        return False, str_i
                            elif match_str.find(string[str_i]) > -1:
                                consumed_list.append(1)
                                str_i += 1
                            else:
                                can_bt, bt_str_i = backtrack(
                                    backtrack_stack, before_str_i)
                                if can_bt:
                                    str_i = bt_str_i
                                    backtracking = True
                                    break
                                else:
                                    return False, str_i
                        else:  # finished input
                            # finished input w/o finishing the re tree
                            if min_ <= j:
                                break
                            else:
                                # i have more states, but the input is finished
                                can_bt, bt_str_i = backtrack(
                                    backtrack_stack, before_str_i)
                                if can_bt:
                                    str_i = bt_str_i
                                    backtracking = True
                                    break
                                else:
                                    return False, str_i
                        j += 1
                    if not backtracking:
                        backtrack_stack.append(
                            (curr_tkn, min_, j, consumed_list))
                        i += 1
                    continue
                else:
                    return False, str_i

            return True, str_i
        return match_group(ast=ast, string=string)
