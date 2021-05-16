# Q1

The regular expression is first preprocessed. '.' is added to each place where concatenation is happening. The regex is then converted to post-fix format. After conversion, stack is used to find the nfa. The nfa of each string literal is found piece by piece and then joined together according to the type of operation to be performed i.e., '\*', '+' or '.'.

# Q2

In this an NFA is changed to a DFA. If there are n states in the NFA, all the 2^n states are generated for te DFA considering every linear combination of the NFA states. Start State of the DFA becomes the epsilon cover of the start state of the NFA. For a transition each letter is considered followed by epsilon movements i.e., transitions of the format of (a letter)$$$ (any number of $s)

# Q3

In this a DFA is converted to its regular expression. Initially two new states QStart and Qend are added to the DFA to ensure that there is only one final state (sink) and only one start state (source). Then, a state is chosen to be removed from the original set of states. When removing all the state transitions from that state are considered. For each input state and output state a new connection is made with weight (input_regex)(loop)\*(ouput_regex). If there are multiple input transitions from a single state to the target state, then we take union of the regex of all the transitions. The same is done for output transitions. At the end only the transitions between QStart and QEnd are left and the final regex is the union of the regex of all these QStart and QEnd transitions.

# Q4

In this we have to convert DFA to optimal DFA. Initially the unreachable states are removed by DFS starting from the start state. Then all the reachable states are split into 2 sets: final and non-final states. At each iteration we randomly choose a set and try to split it into two non-empty sets such that transition from set goes to target set whereas for the other it doesnt. This splitting continues until no longer such partitions can be done and we get the final set of partitions which constitute the states in the optimized DFA.
