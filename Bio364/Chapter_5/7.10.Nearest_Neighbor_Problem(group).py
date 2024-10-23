import sys
from typing import List, Dict, Tuple
import numpy as np
from copy import deepcopy

def NearestNeighbor(a: int, b: int, adjacency_list: Dict[int, List[int]]) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
    '''
    Code Challenge: Solve the Nearest Neighbors of a Tree Problem.

    Input: Two internal nodes a and b specifying an edge e, followed by an adjacency list of an unrooted binary tree.
    Output: Two adjacency lists representing the nearest neighbors of the tree with respect to e. Separate the 
    adjacency lists with a blank line.
    '''

    #print(adjacency_list[a])
    #print(adjacency_list[b])

    #swap: a[3] with b[1]
    #make tree 

    #swap: a[3] with b[0]
    #make tree

    x = 0
    x_pos = 0

    for i in range(len(adjacency_list[a])):
        #print(adjacency_list[a][i])
        if adjacency_list[a][i] != b:
            x = adjacency_list[a][i]
            x_pos = i
            break
   
    #print(x_pos)
    #x = 3
    for i in range(len(adjacency_list[b])):
        #print(adjacency_list[a][i])
        if adjacency_list[b][i] != a:
            y = adjacency_list[b][i]
            y_pos = i
            break

    for i in range(len(adjacency_list[b])):
        #print(adjacency_list[a][i])
        if adjacency_list[b][i] != a and adjacency_list[b][i] != y:
            z = adjacency_list[b][i]
            z_pos = i
            break

    #y = adjacency_list[b][0] #0
    #z = adjacency_list[b][1] #1
    print(y)
    print(z)

    #swap x with y and x with z, results in 2 new trees

    adjacency_list1 = deepcopy(adjacency_list)
    adjacency_list2 = deepcopy(adjacency_list)
    
    adjacency_list1[b][y_pos] = x  #swap y for x
    adjacency_list1[a][x_pos] = y
    adjacency_list1[x].remove(a)
    adjacency_list1[x].append(b)
    adjacency_list1[y].remove(b)
    adjacency_list1[y].append(a)

    adjacency_list2[b][z_pos] = x #swap z for x
    adjacency_list2[a][x_pos] = z
    adjacency_list2[x].remove(a)
    adjacency_list2[x].append(b)
    adjacency_list2[z].remove(b)
    adjacency_list2[z].append(a)

    return adjacency_list1, adjacency_list2

def print_tree(tree: dict[int, list[int]]):
    for key in tree:
        for item in tree[key]:
            print(f"{key}->{item}")
    print("")

tree_adjacency = {
    5: [4, 3, 2], #a - w,x
    4: [5, 0, 1], #b - y,z #NOTE: SHOULD HAVE ANOTHER VAL 5
    3: [5], #w - a
    2: [5], #x - a
    1: [4], #y - b
    0: [4] #z - b
}

a = 32
b = 57

#print_tree(list1)
#print_tree(list2)
#print_tree(tree_adjacency)

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


list1, list2 = NearestNeighbor(a, b, adj_list)
print_tree(list1)
print_tree(list2)