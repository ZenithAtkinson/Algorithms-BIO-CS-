import sys
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
    for i in states:
        viterbi[i] = {"x" + str(i): 0 for i in range(len(string_x))}

    source_probs = 1 / len(states)

    viterbi[states[0]][x_alphabet[0]] = .5    
    print(viterbi)


    

    pass




input = "ABABBBAAAA\nA B\nA	BA	0.377	0.623B	0.26	0.74"
string_x = "xyxzzxyxyy"
x_alphabet = ["x","y","z"]
states = ["A", "B"]
transition_matrix = {
    "A": {"A": 0.641, "B": 0.359},
    "B": {"A": 0.729, "B": 0.271}
}
emission_matrix = {
    "A": {"x": 0.117, "y": 0.691, "z": 0.192},
    "B": {"x": 0.097, "y": 0.42, "z": 0.483}
}

viterbi_algorithm_for_decoding(string_x, x_alphabet, states, transition_matrix, emission_matrix)