import json
import sys

nfa_file = sys.argv[1]
dfa_file = sys.argv[2]

with open(nfa_file) as f:
    nfa_data = json.load(f)

transition_matrix = nfa_data["transition_function"]

# pre_transition_list = {}
transition_list = {}
epsilon_cover = {}

for all_state in nfa_data["states"]:
    epsilon_cover[all_state] = []
    # pre_transition_list[all_state] = {}
    transition_list[all_state] = {}
    for letter in nfa_data["letters"]:
        # pre_transition_list[all_state][letter] = []
        transition_list[all_state][letter] = []
    # pre_transition_list[all_state]["$"] = []
    transition_list[all_state]["$"] = []

for transition in transition_matrix:
    start_state = transition[0]
    inp_char = transition[1]
    final_state = transition[2]
    transition_list[start_state][inp_char].append(final_state)

# print(pre_transition_list)
# print("--------------------------------------------------")

for state in nfa_data["states"]:
    visited = {}
    for all_state in nfa_data["states"]:
        visited[all_state] = 0
    visited[state] = 1
    stack = [state]
    while len(stack):
        s = stack.pop()
        epsilon_cover[state].append(s)
        if visited[s] == 0:
            visited[s] = 1

        for node in transition_list[s]['$']:
            if visited[node] == 0:
                stack.append(node)

for state in transition_list.keys():
    for letter in nfa_data["letters"]:
        if letter == '$':
            continue
        visited = {}
        for all_state in nfa_data["states"]:
            visited[all_state] = 0
        visited[state] += 1
        stack = []
        direct_states = transition_list[state][letter]
        for final_state in direct_states:
            if not visited[final_state]:
                visited[final_state] += 1
                stack.append(final_state)
                while len(stack):
                    s = stack.pop()
                    transition_list[state][letter].append(s)
                    if visited[s] != 2:
                        visited[s] += 1

                    for node in transition_list[s]['$']:
                        if visited[node] != 2:
                            stack.append(node)

        transition_list[state][letter] = list(set(transition_list[state][letter]))

# print(epsilon_cover)
# print(pre_transition_list)
# for state in nfa_data["states"]:
#     for letter in nfa_data["letters"]:
#         for epsilon_state in epsilon_cover[state]:
#             transition_list[state][letter].extend(pre_transition_list[epsilon_state][letter])
#         transition_list[state][letter] = list(set(transition_list[state][letter]))
# print(transition_list)

final_states = nfa_data["final_states"]

dfa_states = []
dfa_final_states = []
dfa_transition = []
num_states = 2 ** len(nfa_data["states"])
num_bits = len(nfa_data["states"])

for state_num in range(num_states):
    bit_mask = [state_num & (1 << bit) for bit in range(num_bits)]
    state = ['Q' + str(i) for i in range(len(bit_mask)) if bit_mask[i] != 0]
    dfa_states.append(state)
    if set(final_states) & set(state):
        dfa_final_states.append(state)
    for let in nfa_data["letters"]:
        l_transition = []
        for s in state:
            l_transition.extend(transition_list[s][let])
        l_transition = list(set(l_transition))
        l_transition = sorted(l_transition, key=lambda x: x)
        dfa_transition.append([state, let, l_transition])

final_dfa = {"states": dfa_states, "letters": sorted(nfa_data["letters"], key=lambda x: x),
             "transition_function": sorted(dfa_transition, key=lambda x: x[0]),
             "start_states": [epsilon_cover[nfa_data["start_states"][0]]],
             "final_states": sorted(dfa_final_states, key=lambda x: x)}

# fans = {
#     'states': [],
#     'transition_function': [],
#     'start_states': [],
#     'final_states': [],
#     'letters': nfa_data["letters"],
# }


# def format(state):
#     state.sort()
#     return ''.join(state)


# for state in final_dfa['states']:
#     fans['states'].append(format(state))

# for state in final_dfa['start_states']:
#     fans['start_states'].append(format(state))

# for state in final_dfa['final_states']:
#     fans['final_states'].append(format(state))

# for transition in final_dfa['transition_function']:
#     fans['transition_function'].append(
#         [format(transition[0]), transition[1], format(transition[2])])

with open(dfa_file, 'w') as f:
    json.dump(final_dfa, f)
