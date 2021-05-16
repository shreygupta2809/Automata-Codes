import json
import sys

dfa_file = sys.argv[1]
regex_file = sys.argv[2]

with open(dfa_file) as f:
    dfa_data = json.load(f)

num_states = len(dfa_data["states"])

for final_state in dfa_data["final_states"]:
    dfa_data["transition_function"].append([final_state, '$', "QEnd"])
for start_state in dfa_data["start_states"]:
    dfa_data["transition_function"].append(["QStart", '$', start_state])

transitions = dfa_data["transition_function"]

for state_num in range(num_states):
    state = dfa_data["states"][state_num]
    # print(transitions)
    # print(state)
    # print("--------------------------------")
    out_transitions = {}
    in_transitions = {}
    loop_string = ""
    for transition in transitions:
        outgoing_state = transition[0]
        incoming_state = transition[2]
        if outgoing_state == state and incoming_state == state:
            if loop_string != "":
                loop_string += '+' + transition[1]
            else:
                loop_string += transition[1]
        elif outgoing_state == state:
            if incoming_state in out_transitions:
                out_transitions[incoming_state] += '+' + transition[1]
            else:
                out_transitions[incoming_state] = transition[1]
        elif incoming_state == state:
            if outgoing_state in in_transitions:
                in_transitions[outgoing_state] += '+' + transition[1]
            else:
                in_transitions[outgoing_state] = transition[1]
    # print(out_transitions)
    # print(in_transitions)
    # print(loop_string)
    # print("==============================")
    for in_state in in_transitions:
        for out_state in out_transitions:
            reg_char = ""
            if loop_string != "":
                reg_char += '(' + in_transitions[in_state] + ').(' + loop_string + ')*' + '.(' + \
                            out_transitions[out_state] + ')'
            else:
                reg_char += '(' + in_transitions[in_state] + ').(' + out_transitions[out_state] + ')'
            transitions.append([in_state, reg_char, out_state])

    final_transitions_index = []
    for i in range(len(transitions)):
        transit = transitions[i]
        if transit[0] == state or transit[2] == state:
            final_transitions_index.append(i)

    transitions = [j for i, j in enumerate(transitions) if i not in final_transitions_index]

# print(transitions)
pre_regex = ""
for transit in transitions:
    pre_regex += transit[1] + '+'

pre_regex = pre_regex[:-1]
pre_regex = pre_regex.replace('.', '')
regex = ""
for i in range(len(pre_regex)):
    if i < len(pre_regex) - 2 and pre_regex[i] == '(' and pre_regex[i + 2] == ')':
        continue
    if i >= 2 and pre_regex[i] == ')' and pre_regex[i - 2] == '(':
        continue
    regex += pre_regex[i]

regex_final = ""
for i in range(len(regex)):
    if i < len(regex) - 1 and regex[i] == '$' and (regex[i + 1] in dfa_data["letters"] or regex[i + 1] == '('):
        continue
    if i >= 1 and regex[i] == '$' and (regex[i - 1] == '*' or regex[i - 1] == ')' or regex[i - 1] in dfa_data["letters"]):
        continue
    regex_final += regex[i]

if regex_final == "":
    regex_final += '$'
final_regex = {"regex": regex_final}

with open(regex_file, 'w') as f:
    json.dump(final_regex, f)
