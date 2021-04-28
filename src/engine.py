import numpy as np
from .pyrser import Pyrser
from .re_ast import ASTNode, Element, GroupNode, LeafNode, NotNode, OrNode, RangeElement, RE, WildcardElement

# no backtracking or equivalent strategy applied yet :(
class RegexEngine:
    def __init__(self):
        self.parser = Pyrser()

    def match(self, re: str, string: str):
        ast = self.parser.parse(re=re)
        prev_node = None
        curr_tkn = ast
        str_i = 0  # matched string chars so far

        def match_group(ast: ASTNode, string: str):
            '''
            Match a group, which is always the case.

            Use recursion when it meets a OrNode.

            Returns the match state (True or False) and the new string i, that is the
            number of matched characters in the string so far.
            '''
            nonlocal str_i
            # curr_tkn here is always a group or ornode
            # because recursion occur only w/ OrNode,
            # which
            curr_tkn = ast.children[0]
            i = 0  # the children i'm iterating, not to confuse with str_i

            # the passed ast can't be a Leaf
            while i < len(ast.children):
                # if str_i == len(string) - 1:
                # i consumed all the input string
                #    break

                # if is OrNode I evaluate the sub-groups with a recursive call
                if isinstance(curr_tkn, OrNode):
                    res, new_str_i = match_group(ast=ast.left, string=string)

                    if res == True:
                        # yeah it's true, I'm done w/ this or!!
                        str_i = new_str_i  # update the consumed characters
                        i += 1  # iterate the next child
                        continue
                    else:
                        # nooo I must try the other one :(
                        res, new_str_i = match_group(
                            ast=ast.right, string=string)
                        if res == True:
                            # yeah!
                            str_i = new_str_i
                            i += 1
                            continue
                        else:
                            # no match :(
                            # new_str_i and not str_i so to inform exactly about where the fail occurred
                            return False, new_str_i

                elif isinstance(curr_tkn, GroupNode):
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    j = 0
                    while j < max_:
                        # aaaaah the group numerosity! Sh***t!
                        res, new_str_i = match_group(
                            ast=curr_tkn, string=string)
                        if res == True:
                            # yes! Come on!
                            str_i = new_str_i
                            i += 1
                        elif j < min_:
                            # no match sorry :(
                            return False, new_str_i
                        else:
                            break
                        j += 1
                    continue

                else:
                    # it is a LeafNode obviously now
                    min_, max_ = curr_tkn.min, curr_tkn.max
                    j = 0
                    while j < max_:
                        match_str = curr_tkn.match if not type(
                            curr_tkn) is WildcardElement else True
                        if str_i < len(string) - 1:  # i still have input to match
                            if type(match_str) is bool:
                                # i have a wildcard baby
                                str_i += 1
                            elif match_str.find(str_i[i+1]) > -1:
                                str_i += 1
                            elif:
                                return False, str_i
                        else:  # finished input
                            # finished input w/o finishing the re tree
                            if min_ <= j:
                                i += 1
                                continue
                            else:
                                # i have more states, but the input is finished
                                return False, str_i

            return True, str_i
        return match_group(ast=ast, string=string)
