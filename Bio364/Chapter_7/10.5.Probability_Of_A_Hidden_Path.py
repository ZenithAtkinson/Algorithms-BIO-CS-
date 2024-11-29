import sys
from typing import List, Dict, Iterable, Tuple, Set

def probability_of_hidden_path(hidden_path: str, states: str, transition_matrix: Dict[str, Dict[str, float]]):
    '''
    Input: A hidden path π followed by the states States and transition matrix Transition of an HMM (Σ, States, Transition, Emission).
    Output: The probability of this path, Pr(π).
    '''

    prob = .5

    for i in range(1, len(hidden_path)):
        prev_state = hidden_path[i-1]
        current_state = hidden_path[i]
        #print(prev_state)
        #print(current_state)
        #print(transition_matrix[prev_state][current_state])
        prob *= transition_matrix[prev_state][current_state]
    return prob


input = "ABABBBAAAA\nA B\nA	BA	0.377	0.623B	0.26	0.74"
h = "AAABAAAAAAAAABAAAABBABBAABAABBABBABABBAABBABABBBAA"
s = ["A", "B"]
t = {
    "A": {"A": 0.503, "B": 0.497},
    "B": {"A": 0.52, "B": 0.48}
}

print(probability_of_hidden_path(h, s, t))
