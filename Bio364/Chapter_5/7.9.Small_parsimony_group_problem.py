import sys
from typing import List, Dict, Tuple
import numpy as np


def SmallParsimony(n: int,  adjacency_list: dict) -> Tuple[int, dict]:
    '''
    Input: An integer n followed by an adjacency list for a rooted binary tree with n leaves labeled by DNA strings.
    Output: The minimum parsimony score of this tree, followed by the adjacency list of a tree corresponding to 
        labeling internal nodes by DNA strings in order to minimize the parsimony score of the tree.  You may break 
        ties  however you like.
    '''
    #print(adjacency_list)
    score = 0
    tags = {}
    for node in adjacency_list:
        #print(node) # prints 4, 5, 6
        tags[node] = 0
        if type(adjacency_list[node][1]) == str:
            tags[node] = 1
    
    pass


n = 4

adjacency_list = {
    4: ["CAAATCCC", "ATTGCGAC"],
    5: ["CTGCGCTG", "ATGGACGA"],
    6: [4, 5]
}

#print(type(adjacency_list))
SmallParsimony(n, adjacency_list)

with open('dataset.txt', 'r') as file:
    adj_list = {}

    for line in file:
        
        line = line.strip()
        #print(line.strip())
        result = line.split("->")
        if len(result) != 2:
            continue
        #print(result)
        if "A" in result[1]:
            value = result[1]
        else:
            value = int(result[1])
        if int(result[0]) not in adj_list:
            adj_list[int(result[0])] = [value]
        else:
            adj_list[int(result[0])].append(value)

        print(adj_list)

#print(content)

#def organize_data(text):
#    for line in text:
#    print(line)

''' Pseudocode:
SmallParsimony(T, Character)
    for each node v in tree T
        Tag(v) ← 0
        if v is a leaf
            Tag(v) ← 1
            for each symbol k in the alphabet
                if Character(v) = k
                    sk(v) ← 0
                else
                    sk(v) ← ∞
    while there exist ripe nodes in T
        v ← a ripe node in T
        Tag(v) ← 1
        for each symbol k in the alphabet
            sk(v) ← minimumall symbols i {si(Daughter(v))+αi,k} + minimumall symbols j {sj(Son(v))+αj,k}
    return minimum over all symbols k {sk(v)}
'''