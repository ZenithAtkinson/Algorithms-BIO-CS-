import sys
import pandas as pd
from typing import List, Dict, Iterable, Tuple, Set

def viterbi_outcome_likelihood_problem(string_x: str, x_alphabet: str, states: str, transition_matrix: Dict[str, Dict[str, float]], emission_matrix: Dict[str, Dict[str, float]]):
    '''
    Input: A string x, followed by the alphabet from which x was constructed, followed by the states States, transition matrix Transition, and emission matrix Emission of an HMM (Σ, States, Transition, Emission).
    Output: The probability Pr(x) that the HMM emits x.
    '''
    viterbi = {}
    for state in states:
        viterbi[state] = [0] * len(string_x)


    source_probs = (1 / len(states))
    #First row:
    for state in states:
        viterbi[state][0] = emission_matrix[state][string_x[0]] * source_probs
    df = pd.DataFrame(viterbi).T
    #print(df)

    for t in range(1, len(string_x)):
        for state in states:
            #print(state, ": ", viterbi[state][t])
            for other_state in states:
                viterbi[state][t] += viterbi[other_state][t-1] * transition_matrix[other_state][state]
            viterbi[state][t] *= emission_matrix[state][string_x[t]]

    sum = 0
    for i in viterbi:
        sum += viterbi[i][-1]
    return(sum)



string_x = "xyxxyxzzxzxxxyxxyyzxyyyxxzyxyyzxxyyxxyyyzyzyxyzyzyyzzxxxxzxzzzxyxxxzyxxyxzxyyyxxyyzyyzxxzyyxxxxyzxxy"
x_alphabet = ["x","y","z"]
states = ["A", "B", "C", "D"]
transition_matrix = {
    "A": {"A": 0.216, "B": 0.361, "C": 0.412, "D": 0.011},
    "B": {"A": 0.396, "B": 0.417, "C": 0.013, "D": 0.174},
    "C": {"A": 0.296, "B": 0.228, "C": 0.179, "D": 0.297},
    "D": {"A": 0.013, "B": 0.63, "C": 0.274, "D": 0.083},
}

emission_matrix = {
    "A": {"x": 0.481, "y": 0.047, "z": 0.472},
    "B": {"x": 0.354, "y": 0.272, "z": 0.374},
    "C": {"x": 0.299, "y": 0.247, "z": 0.454},
    "D": {"x": 0.429, "y": 0.42, "z": 0.151},
}

print(viterbi_outcome_likelihood_problem(string_x, x_alphabet, states, transition_matrix, emission_matrix))