import sys
from typing import List, Dict, Tuple
import numpy as np

def neighbor_joining(n: int,  distance_matrix: List[List[int]]) -> List[str]:
    '''
    Input: An integer n, followed by an n x n distance matrix.
    Output: An adjacency list for the tree resulting from applying the neighbor-joining algorithm. 
        Edge-weights should be accurate to two decimal places (they are provided to three decimal places in the sample output below).
    '''

    

    pass

#pass:
#dict[int, list[int]]
#return:
#dict[int, dict[int, float]]


n = 4
distance_matrix = [
    [0, 23, 27, 20],
    [23, 0, 30, 28],
    [27, 30, 0, 30],
    [20, 28, 30, 0]
]
print(neighbor_joining(n ,distance_matrix))

