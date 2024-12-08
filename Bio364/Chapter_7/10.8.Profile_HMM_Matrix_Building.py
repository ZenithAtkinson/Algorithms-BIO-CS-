import contextlib
import sys
from collections import defaultdict
import pandas as pd
from typing import List, Dict, Iterable, Tuple, Set
from tempCodeRunnerFile import printer_i_hardly_know_her, print_HMM

def multiple_alignment_HMM(theta: float, sigma: float, alphabet: List[str], alignment: List[str]):
    '''
    Input: A threshold θ and a pseudocount σ, followed by an alphabet Σ, followed by a multiple alignment Alignment whose strings are formed from Σ.
    Output: The transition and emission matrices of HMM(Alignment, θ, σ).
    '''
    n = len(alignment)
    m = len(alignment[0])
    

    gapped = [0] * m
    for row in alignment:
        for i, char in enumerate(row):
            if char == '-':
                gapped[i] += 1
    gap_fracs = [gc / n for gc in gapped]
    print(gap_fracs)
    
    matches = []
    for i, frac in enumerate(gap_fracs):
        if frac < theta:
            matches.append(i) #OG alignment vs new alignment

    #match_columns = [i for i, frac in enumerate(gap_fracs) if frac < theta]
    k = len(matches)
    
    # states: S, I0, M1..Mk, D1..Dk, I1..Ik, E
    states = ['S', 'I0'] #Init with the starting and I0
    for i in range(1, k + 1):
        states.extend([f"M{i}", f"D{i}", f"I{i}"])
    states.append('E')

    #stateIes = {}
    #for idx, state in enumerate(states):
    #    stateIes[state] = idx


    TRANSITION_counts = {}
    EMISSION_counts = {}
    state_visit_counts = {}
    state_EMISSION_counts = {}
    
    for row in alignment:
        #print(row)
        last_state = 'S'
        if last_state not in TRANSITION_counts:
            TRANSITION_counts[last_state] = {}
        if last_state not in state_visit_counts:
            state_visit_counts[last_state] = 0
        state_visit_counts[last_state] += 1

        current_match_idx = 0  # Where we are

        for col_idx, char in enumerate(row):
            #print(col_idx, "+", char)
            if col_idx in matches:
                current_match_idx += 1
                if char == '-':
                    #Go delete it
                    cur_state = f"D{current_match_idx}"
                else:
                    #Go match it
                    cur_state = f"M{current_match_idx}"

                    if cur_state not in EMISSION_counts: #Matrix consturction
                        EMISSION_counts[cur_state] = {}
                    if char not in EMISSION_counts[cur_state]:
                        EMISSION_counts[cur_state][char] = 0
                    EMISSION_counts[cur_state][char] += 1

                    if cur_state not in state_EMISSION_counts: #Matrix consturction
                        state_EMISSION_counts[cur_state] = 0
                    state_EMISSION_counts[cur_state] += 1
                    #print(state_EMISSION_counts)
            else:
                if char == '-':
                    #Deleted, skip
                    continue
                else:
                    # Insertion state
                    cur_state = f"I{current_match_idx}"

                    if cur_state not in EMISSION_counts: #Matrix consturction
                        EMISSION_counts[cur_state] = {}
                    if char not in EMISSION_counts[cur_state]:
                        EMISSION_counts[cur_state][char] = 0
                    EMISSION_counts[cur_state][char] += 1
                    if cur_state not in state_EMISSION_counts: #Matrix consturction
                        state_EMISSION_counts[cur_state] = 0
                    state_EMISSION_counts[cur_state] += 1
                    #print(state_EMISSION_counts)
            
            if last_state not in TRANSITION_counts:
                TRANSITION_counts[last_state] = {}
            if cur_state not in TRANSITION_counts[last_state]:
                TRANSITION_counts[last_state][cur_state] = 0
            TRANSITION_counts[last_state][cur_state] += 1
            # increase visit count for dividing
            if cur_state not in state_visit_counts:
                state_visit_counts[cur_state] = 0
            state_visit_counts[cur_state] += 1

            last_state = cur_state
        
        # END state:
        if last_state not in TRANSITION_counts:
            TRANSITION_counts[last_state] = {}
        if 'E' not in TRANSITION_counts[last_state]:
            TRANSITION_counts[last_state]['E'] = 0
        TRANSITION_counts[last_state]['E'] += 1
        if 'E' not in state_visit_counts:
            state_visit_counts['E'] = 0
        state_visit_counts['E'] += 1
    
    #Needed for I0
    for state in states:
        if state not in TRANSITION_counts:
            TRANSITION_counts[state] = {}
    
    trans_mans = []
    for s in states:
        row = []
        total_out = sum(TRANSITION_counts[s].values())
        for t in states:
            if t in TRANSITION_counts[s]:
                if total_out > 0:
                    prob = TRANSITION_counts[s][t] / total_out
                else:
                    prob = 0.0
            else:
                prob = 0.0
            row.append(prob)
        trans_mans.append(row)
    
    
    emission_mans = []
    for s in states:
        row = []
        if s.startswith('M') or s.startswith('I'):
            total_emit = state_EMISSION_counts.get(s, 0) + sigma * len(alphabet)
            for sym in alphabet:
                #print(sym)
                #print(s)
                count = EMISSION_counts.get(s, {}).get(sym, 0)
                prob = (count + sigma) / total_emit
                row.append(prob)
        else:
            # Nothing states
            row = [0.0] * len(alphabet)
        emission_mans.append(row)
    
    return states, trans_mans, emission_mans

sample_input = """0.289
--------
A B C D E
--------
EBA
E-D
EB-
EED
EBD
EBE
E-D
E-D"""
thet = 0.358
alpha = ['A', 'B', 'C', 'D', 'E']
alphabetINstring = """
A-A
ADA
ACA
A-C
-EA
D-A
"""
sig = .01

Align = alphabetINstring.splitlines()
Align = Align[1:]
#print(Align)
    
states, trans_mans, emissions = multiple_alignment_HMM(thet, sig, alpha, Align)
    
#printer_i_hardly_know_her(trans_mans)
print(emissions)

print_HMM(states, trans_mans, emissions, alpha)
with open("output.txt", "w") as f:
        with contextlib.redirect_stdout(f):
            print_HMM(states, trans_mans, emissions, alpha)