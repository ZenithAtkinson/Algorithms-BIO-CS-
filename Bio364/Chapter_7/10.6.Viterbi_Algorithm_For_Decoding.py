import sys
import pandas as pd
from typing import List, Dict, Iterable, Tuple, Set

def viterbi_algorithm_for_decoding(string_x: str, x_alphabet: str, states: str, transition_matrix: Dict[str, Dict[str, float]], emission_matrix: Dict[str, Dict[str, float]]):
    '''
    Input: A string x, followed by the alphabet from which x was constructed, followed by the states States, transition matrix Transition, and emission matrix Emission of an HMM (Σ, States, Transition, Emission).
    Output: A path that maximizes the (unconditional) probability Pr(x, π) over all possible paths π.
    '''
    # Setting up da backtrack
    empty_lists = [[] for _ in range(len(string_x))]

    backtrack = {}
    for val in states:
        backtrack[val] = empty_lists.copy()
    #print(backtrack)
    # From source node to sink node, where they are blank nodes...
    # Max the probability

    #For each val i in the string...
    #It is equal to i-1 * i state probability * i transmission probability.
    #Put this in viterbi matrix (which is just the graph)
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
            max_prob = 0  # Store the maxinum probability
            best_prev_state = None#yet
            for prev_state in states:
                prob = viterbi[prev_state][t - 1] * transition_matrix[prev_state][state]
                if prob > max_prob:
                    max_prob = prob
                    best_prev_state = prev_state
            viterbi[state][t] = max_prob * emission_matrix[state][string_x[t]]
            backtrack[state][t] = best_prev_state

    final_probs = {state: viterbi[state][-1] for state in states}
    last_state = max(final_probs, key=final_probs.get)

    path = [last_state]
    for t in range(len(string_x) - 1, 0, -1):
        path.append(backtrack[path[-1]][t])
    path.reverse()

    #for c in path:
    #    print(c, end ="")

    return path


input = "ABABBBAAAA\nA B\nA	BA	0.377	0.623B	0.26	0.74"
string_x = "zzxxzyyxzxxzyzyxzyyyyxzxzzzzzyxyxzyxxxzzyxyyyzxyxzxxzxxzxyzzxzyyyzzyxzxxyyzxxyxzzyxyxxyyxxxzzyzyyyyz"
x_alphabet = ["x","y","z"]
states = ["A", "B"]
transition_matrix = {
    "A": {"A": 0.173, "B": 0.827},
    "B": {"A": 0.289, "B": 0.711}
}
emission_matrix = {
    "A": {"x": 0.456, "y": 0.1, "z": 0.444},
    "B": {"x": 0.31, "y": 0.429, "z": 0.261}
}

print(viterbi_algorithm_for_decoding(string_x, x_alphabet, states, transition_matrix, emission_matrix))