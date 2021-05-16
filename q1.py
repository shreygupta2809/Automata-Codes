import copy
import json
import sys

regex_file = sys.argv[1]
nfa_file = sys.argv[2]

with open(regex_file) as f:
    regular_expression_data = json.load(f)

pre_regular_expression = "".join(regular_expression_data["regex"].split())


def char_check(input_char):
    if input_char == ')':
        return 1
    if input_char == '(':
        return 2
    if input_char == '+':
        return 3
    if input_char == '.':
        return 4
    if input_char == '*':
        return 5
    return 0


pre_post_regular_expression = ""
for i in range(len(pre_regular_expression) - 1):
    cur_char = pre_regular_expression[i]
    next_char = pre_regular_expression[i + 1]
    pre_post_regular_expression += cur_char
    if (char_check(cur_char) == 0 and char_check(next_char) == 0) or (
            char_check(cur_char) == 0 and char_check(next_char) == 2) or (
            char_check(cur_char) == 1 and char_check(next_char) == 0) or (
            char_check(cur_char) == 5 and char_check(next_char) == 0) or (
            char_check(cur_char) == 5 and char_check(next_char) == 2) or (
            char_check(cur_char) == 1 and char_check(next_char) == 2):
        pre_post_regular_expression += '.'

pre_post_regular_expression += pre_regular_expression[-1]

post_fix_stack = []
regular_expression = ""

for i in pre_post_regular_expression:
    if char_check(i) == 0:
        regular_expression += i
    elif i == '(':
        post_fix_stack.append(i)
    elif i == '*':
        regular_expression += i
    elif i == ')':
        while len(post_fix_stack) and post_fix_stack[-1] != '(':
            regular_expression += post_fix_stack[-1]
            post_fix_stack.pop()
        post_fix_stack.pop()
    else:
        if len(post_fix_stack) == 0 or char_check(i) > char_check(post_fix_stack[-1]):
            post_fix_stack.append(i)
        else:
            while len(post_fix_stack) and char_check(i) <= char_check(post_fix_stack[-1]):
                regular_expression += post_fix_stack[-1]
                post_fix_stack.pop()
            post_fix_stack.append(i)

while len(post_fix_stack):
    regular_expression += post_fix_stack[-1]
    post_fix_stack.pop()

state_number = 0


def concat(left, right):
    new_dict = copy.deepcopy(left)
    new_dict["states"].extend(right["states"])
    new_dict["letters"].extend(right["letters"])
    new_dict["letters"] = list(set(new_dict["letters"]))
    new_dict["transition_function"].extend(right["transition_function"])
    for state in left['final_states']:
        for start_state in right['start_states']:
            new_dict["transition_function"].append([state, '$', start_state])
    new_dict["final_states"] = copy.deepcopy(right["final_states"])
    return new_dict


def star(dict1, index):
    new_dict = copy.deepcopy(dict1)
    new_dict["states"].append('Q' + str(index))
    new_dict["transition_function"].append(['Q' + str(index), '$', dict1["start_states"][-1]])
    for state in dict1["final_states"]:
        for start_state in dict1["start_states"]:
            new_dict["transition_function"].append([state, '$', start_state])
    new_dict["start_states"] = ['Q' + str(index)]
    new_dict["final_states"].append('Q' + str(index))
    index += 1
    return new_dict, index


def union(left, right, index):
    new_dict = copy.deepcopy(left)
    new_dict["states"].extend(right["states"])
    new_dict["states"].append('Q' + str(index))
    new_dict["letters"].extend(right["letters"])
    new_dict["letters"] = list(set(new_dict["letters"]))
    new_dict["transition_function"].extend(right["transition_function"])
    for state in left['start_states']:
        new_dict["transition_function"].append(['Q' + str(index), '$', state])
    for state in right['start_states']:
        new_dict["transition_function"].append(['Q' + str(index), '$', state])
    new_dict["final_states"].extend(right["final_states"])
    new_dict["start_states"] = ['Q' + str(index)]
    index += 1
    return new_dict, index


nfa_stack = []

for seq_char in regular_expression:
    if seq_char == '+':
        top_dict_left = nfa_stack.pop()
        top_dict_right = nfa_stack.pop()
        temp_dict, state_number = union(top_dict_left, top_dict_right, state_number)
        nfa_stack.append(temp_dict)
    elif seq_char == '*':
        top_dict = nfa_stack.pop()
        temp_dict, state_number = star(top_dict, state_number)
        nfa_stack.append(temp_dict)
    elif seq_char == '.':
        top_dict_right = nfa_stack.pop()
        top_dict_left = nfa_stack.pop()
        nfa_stack.append(concat(top_dict_left, top_dict_right))
    else:
        single_nfa_dict = {"states": ['Q' + str(state_number), 'Q' + str(state_number + 1)],
                           "letters": [seq_char],
                           "transition_function": [['Q' + str(state_number), seq_char, 'Q' + str(state_number + 1)]],
                           "start_states": ['Q' + str(state_number)],
                           "final_states": ['Q' + str(state_number + 1)]}
        state_number += 2
        nfa_stack.append(single_nfa_dict)

final_nfa = nfa_stack.pop()
final_nfa["transition_function"] = sorted(final_nfa["transition_function"], key=lambda x: x[0])
final_nfa["states"] = sorted(final_nfa["states"], key=lambda x: x)
final_nfa["final_states"] = sorted(final_nfa["final_states"], key=lambda x: x)
final_nfa["start_states"] = sorted(final_nfa["start_states"], key=lambda x: x)
final_nfa["letters"] = sorted(final_nfa["letters"], key=lambda x: x)

with open(nfa_file, 'w') as f:
    json.dump(final_nfa, f)
