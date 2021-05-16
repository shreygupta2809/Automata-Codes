import copy
import json
import sys

dfa_file = sys.argv[1]
opt_dfa_file = sys.argv[2]

with open(dfa_file) as f:
    dfa_data = json.load(f)

transition_matrix = dfa_data["transition_function"]
visited = {}
transition_list = {}

for all_state in dfa_data["states"]:
    transition_list[all_state] = {}
    visited[all_state] = 0
    for letter in dfa_data["letters"]:
        transition_list[all_state][letter] = []
    transition_list[all_state]["$"] = []

for transition in transition_matrix:
    start_state = transition[0]
    inp_char = transition[1]
    final_state = transition[2]
    transition_list[start_state][inp_char].append(final_state)

start_state = dfa_data["start_states"][0]
visited[start_state] = 1

stack = [start_state]
while len(stack):
    s = stack.pop()
    if visited[s] == 0:
        visited[s] = 1

    for letter in dfa_data["letters"]:
        for node in transition_list[s][letter]:
            if visited[node] == 0:
                stack.append(node)

reachable_states = set([state for state in dfa_data["states"] if visited[state] == 1])

initial_set = set([state for state in reachable_states if state not in dfa_data["final_states"]])
final_set = set([state for state in reachable_states if state in dfa_data["final_states"]])
partitions = [copy.deepcopy(initial_set), copy.deepcopy(final_set)]
possible = [copy.deepcopy(initial_set), copy.deepcopy(final_set)]

while len(possible) > 0:
    target_set = possible.pop(0)
    for letter in dfa_data["letters"]:
        lead_to_target_set = set([])
        for state in reachable_states:
            if transition_list[state][letter][0] in target_set:
                lead_to_target_set.add(state)
        for join_part in partitions:
            if len(join_part.intersection(lead_to_target_set)) > 0 and len(join_part - lead_to_target_set) > 0:
                partitions.remove(join_part)
                partitions.append(join_part.intersection(lead_to_target_set))
                partitions.append(join_part - lead_to_target_set)
                if join_part in possible:
                    possible.remove(join_part)
                    possible.append(join_part.intersection(lead_to_target_set))
                    possible.append(join_part - lead_to_target_set)
                else:
                    if len(join_part.intersection(lead_to_target_set)) <= len(join_part - lead_to_target_set):
                        possible.append(join_part.intersection(lead_to_target_set))
                    else:
                        possible.append(join_part - lead_to_target_set)

# print(partitions)
# print(transition_list)

final_states_set = [part for part in partitions if part & set(dfa_data["final_states"])]
start_states_set = [part for part in partitions if part & set(dfa_data["start_states"])]

final_states = []
for f_state in final_states_set:
    # final_state_string = "".join([str(s) for s in f_state])
    # final_states.append(final_state_string)
    final_states.append(list(f_state))

start_states = []
for s_state in start_states_set:
    # start_state_string = "".join([str(s) for s in s_state])
    # start_states.append(start_state_string)
    start_states.append(list(s_state))

states = []
for state in partitions:
    # state_string = "".join([str(s) for s in state])
    # states.append(state_string)
    states.append(list(state))

# print(states)
# print(final_states)
# print(start_states)

transition_function = []
for partition in partitions:
    state = list(partition)
    if len(state) <= 0:
        continue
    for letter in dfa_data["letters"]:
        target = transition_list[state[0]][letter][0]
        target_state = []
        for p in partitions:
            if target in p:
                target_state = list(p)
                break
        transition_function.append([state, letter, target_state])

final_minimal_dfa = {"states": states, "letters": dfa_data["letters"],
                     "transition_function": transition_function,
                     "start_states": start_states, "final_states": final_states}

# fans = {
#     'states': [],
#     'transition_function': [],
#     'start_states': [],
#     'final_states': [],
#     'letters': dfa_data["letters"],
# }


# def format(state):
#     state.sort()
#     return ''.join(state)


# for state in final_minimal_dfa['states']:
#     fans['states'].append(format(state))

# for state in final_minimal_dfa['start_states']:
#     fans['start_states'].append(format(state))

# for state in final_minimal_dfa['final_states']:
#     fans['final_states'].append(format(state))

# for transition in final_minimal_dfa['transition_function']:
#     fans['transition_function'].append(
#         [format(transition[0]), transition[1], format(transition[2])])

with open(opt_dfa_file, 'w') as f:
    json.dump(final_minimal_dfa, f)
