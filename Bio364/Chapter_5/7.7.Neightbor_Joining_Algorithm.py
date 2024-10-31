import sys
from typing import List, Dict, Tuple, Set
import numpy as np

def READ_the_input(file_path: str) -> Tuple[int, Dict[int, Dict[int, float]]]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    n = int(lines[0].strip())
    D = {} #Big D
    for i in range(n):
        #Splitting with whitespace:
        parts = lines[i+1].strip().split()
        D[i] = {}
        for j in range(n):
            D[i][j] = float(parts[j])
    return n, D

def full_neighbor_joining(D: Dict[int, Dict[int, float]], edges: List[int], adj: Dict[int, List[Tuple[int, float]]], next_edge: int) -> Tuple[Dict[int, List[Tuple[int, float]]], int]:
    '''
    Implements the Neighbor-Joining algorithm... but recursively
    Input:
    - D: Current distance matrix (dict of dicts)
    - edges: list of node edges corresponding to rows/columns in D
    - adj: adjacency list (dictionary)
    - next_edge: The next available edge(internal nodes)
    Output:
    - adj: Updated adjacency list + new edges
    - next_edge: Next available edge
    '''
    n = len(edges)
    #If only two nodes left, connect them
    if n == 2:
        i, j = edges[0], edges[1]
        distance = D[i][j]
        
        if i not in adj:
            adj[i] = []
        if j not in adj:
            adj[j] = []
        
        adj[i].append((j, distance))
        adj[j].append((i, distance))
        return adj, next_node
    
    # TOTAL distance of each node
    total_distances = {}
    for i in edges:
        total_distances[i] = sum(D[i][j] for j in edges if j != i)
    
    # Make the D* matrix for finding closest nodes (See first slide of 7.7)
    D_star = {}
    for i in edges:
        D_star[i] = {}
        for j in edges:
            if i == j:
                D_star[i][j] = 0
            else:
                D_star[i][j] = (n - 2) * D[i][j] - total_distances[i] - total_distances[j]
    
    # Smallest elem:
    min_val = float('inf')
    pair = (None, None)
    for i in edges:
        for j in edges:
            if i < j and D_star[i][j] < min_val:
                min_val = D_star[i][j]
                pair = (i, j)
    i, j = pair
    
    #New limb lengths for NEW node
    delta = (total_distances[i] - total_distances[j]) / (n - 2)
    limb_length_i = 0.5 * (D[i][j] + delta)
    limb_length_j = 0.5 * (D[i][j] - delta)

    m = next_node 
    next_node += 1

    # Add new node back in
    D[m] = {}
    for k in edges:
        if k != i and k != j:
            D[m][k] = D[k][m] = 0.5 * (D[k][i] + D[k][j] - D[i][j])
    D[m][m] = 0.0

    # Go back, removing i, j, updating edges and adding new node
    for k in edges:
        if k != i and k != j:
            del D[k][i]
            del D[k][j]
    del D[i]
    del D[j]
    new_edges = [node for node in edges if node != i and node != j]
    new_edges.append(m)

    adj, next_node = full_neighbor_joining(D, new_edges, adj, next_node)
    
    if m not in adj:
        adj[m] = []
    if i not in adj:
        adj[i] = []
    if j not in adj:
        adj[j] = []
    adj[m].append((i, limb_length_i))
    adj[i].append((m, limb_length_i))
    adj[m].append((j, limb_length_j))
    adj[j].append((m, limb_length_j))
    
    return adj, next_node

#---- input readnig and init call
in_file = "data.txt"
n, D = READ_the_input(in_file)


edges = list(range(n))
next_node = n 
adj = {} #Dict

adj, next_node = full_neighbor_joining(D, edges, adj, next_node)

output_edges = []
seen = set()
for u in adj:
    for v, w in adj[u]:
        if (u, v) not in seen and (v, u) not in seen:
            output_edges.append((u, v, w))
            seen.add((u, v))
output_edges.sort() #needed?

#Printing...
for edge in output_edges:
    u, v, w = edge
    w = round(w, 3) #3 decimals
    print(str(u) + "->" + str(v) + ":" + str(w))
    print(str(v) + "->" + str(u) + ":" + str(w))

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
''' old NeighborJoining() (not recusrive by itself)
Input: An integer n, followed by an n x n distance matrix.
Output: An adjacency list for the tree resulting from applying the neighbor-joining algorithm. Edge-weights should be accurate to two decimal places 
(they are provided to three decimal places in the sample output below).
'''
#print(neighbor_joining(n ,distance_matrix))
'''
NeighborJoining(D)
    n ← number of rows in D
    if n = 2
        T ← tree consisting of a single edge of length D1,2
        return T
    D* ← neighbor-joining matrix constructed from the distance matrix D
    find elements i and j such that D*i,j is a minimum non-diagonal element of D*
    Δ ← (TotalDistanceD(i) - TotalDistanceD(j)) /(n - 2)
    limbLengthi ← (1/2)(Di,j + Δ)
    limbLengthj ← (1/2)(Di,j - Δ)
    add a new row/column m to D so that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
    D ← D with rows i and j removed
    D ← D with columns i and j removed
    T ← NeighborJoining(D)
    add two new limbs (connecting node m with leaves i and j) to the tree T
    assign length limbLengthi to Limb(i)
    assign length limbLengthj to Limb(j)
    return T
'''