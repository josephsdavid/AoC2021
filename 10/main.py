from rich import print

open_list = ["[","{","(", "<"]
close_list = ["]","}",")", ">"]


def check(line: str):
    stack = []
    for l in line:
        if l in open_list:
            stack.append(l) # add lhs to stack
        else:
            idx = close_list.index(l)
            # if there are characters in the stack and we match what is in it
            if (len(stack) > 0) and (open_list[idx] == stack[-1]):
                stack.pop() # eliminate the pair
            else:
                # otherwise return the erroneous character
                return l
    if len(stack) == 0:
        return "Complete"
    else:
        return "Incomplete"

def p1_runner(rows):
    score_dict = {")":3, "]":57, "}":1197, ">": 25137}
    out = 0
    for row in rows.splitlines():
        res = check(row)
        if res in score_dict.keys():
            out += score_dict[res]
    print(out)
    return out

from data import test_case, real_deal
p1_runner('()()({}){}[[{}<>]]')
p1_runner(test_case)
p1_runner(real_deal)


def check_v2(line: str):
    stack = []
    for l in line:
        if l in open_list:
            stack.append(l) # add left hand side to the list
        else:
            idx = close_list.index(l)
            # if there is a lhs in stack, and if our character is the match to the end of the stack
            if (len(stack) > 0) and (open_list[idx] == stack[-1]):
                # pop that character out of the stack, we are done with it
                stack.pop()
            else:
                # return the character that made our life hard
                return l
    if len(stack) == 0:
        return ""
    else:
        # return incompleted pairs
        return stack

def p2_runner(rows):
    scores = []
    score_dict = {')':1, ']':2, '}':3, '>': 4}
    for row in rows.splitlines():
        score  = 0
        incomplete= check_v2(row)
        if isinstance(incomplete, list):
            for inc in incomplete[::-1]:
                score *= 5
                score += score_dict[close_list[open_list.index(inc)]]
        scores.append(score)
    scores = [s for s in scores if s != 0]
    #print(scores)
    middle_index = int((len(scores) - 1)/2)
    print(middle_index)
    print(sorted(scores)[middle_index])

p2_runner(test_case)
p2_runner(real_deal)
