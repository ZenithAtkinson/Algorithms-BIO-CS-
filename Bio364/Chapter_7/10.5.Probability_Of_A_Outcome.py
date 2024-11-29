import sys
from typing import List, Dict, Iterable, Tuple, Set

def probability_of_outcome_given_path(input_string_x: str, x_alphabet: str, hidden_path: str, states: str, transition_matrix: Dict[str, Dict[str, float]]):
    '''
    Input: A string x, followed by the alphabet from which x was constructed, followed by a hidden path π, followed by the states States and emission matrix Emission of an HMM (Σ, States, Transition, Emission).
    Output: The conditional probability Pr(x|π) that x will be emitted given that the HMM follows the hidden path π.
    '''
    prob = 1

    for i in range(len(input_string_x)):
        x_char = input_string_x[i]
        state = hidden_path[i]
        prob *= transition_matrix[state][x_char]

    return prob


input = "ABABBBAAAA\nA B\nA	BA	0.377	0.623B	0.26	0.74"
x = "yxzxzzzxyyzyxzzzyzzyzzxzzxzyzzxxxyyyyyzyxyxyzyxzzx"
x_alphabet = ["x","y","z"]
hidden = "BABBAABABAAAAABBABABAABAABBBABBBBAAABAAAAABBBBBBAB"
s = ["A", "B"]
t = {
    "A": {"x": 0.183, "y": 0.453, "z": 0.364},
    "B": {"x": 0.277, "y": 0.312, "z": 0.411}
}

print(probability_of_outcome_given_path(x, x_alphabet, hidden, s, t))