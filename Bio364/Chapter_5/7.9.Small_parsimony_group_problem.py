import sys
from typing import List, Dict, Tuple
import numpy as np
def hamming_distance(suffix: str, text: str) -> int:
    # Returns number of mismatches between two strings
    distance = 0
    if len(suffix) > len(text):
        length = len(text)
        distance = len(suffix) - len(text)
    elif len(suffix) < len(text):
        length = len(suffix)
        distance = len(text) - len(suffix)
    else:
        length = len(suffix)

    for i in range(0, length):
        if suffix[i] != text[i]:
            distance += 1
    return distance


def small_parsimony(n: int, adjacency: dict[int, list]) -> dict:
    tags = {}
    s = {}
    nucs = ["A", "C", "G", "T"]
    for node in adjacency:
        tags[node] = 0
        if type(adjacency[node][0]) == str:
            tags[node] = 1
            for k in nucs:
                print(adjacency[node])
                if k == adjacency[node][0][n] and k == adjacency[node][1][n]:
                    if node in s:
                        s[node].append(0)
                    else:
                        s[node] = [0]
                elif k == adjacency[node][0][n] or k == adjacency[node][1][n]:
                    if node in s:
                        s[node].append(1)
                    else:
                        s[node] = [1]
                else:
                    if node in s:
                        s[node].append(2)
                    else:
                        s[node] = [2]
    path = {}
    for key in adjacency:
        if tags[key] == 1:
            continue
        daughter = s[adjacency[key][0]]
        son = s[adjacency[key][1]]
        for i in range(len(nucs)):
            min_val = -1
            min_pos = []
            for j in range(len(nucs)):
                val = daughter[i] + son[j]
                if i != j:
                    val += 1
                if min_val == -1 or val < min_val:
                    min_val = val
                    min_pos = [i, j]
                val2 = daughter[j] + son[i]
                if i != j:
                    val2 += 1
                if val2 < min_val:
                    min_val = val2
                    min_pos = [j, i]
            if key not in path:
                path[key] = [min_pos]
            else:
                path[key].append(min_pos)
            if key not in s:
                s[key] = [min_val]
            else:
                s[key].append(min_val)
        tags[key] = 1
    #print(path)
    #print(s)
    seq = {}
    start = max(s.keys())
    spot = s[start].index(min(s[start]))
    seq[start] = nucs[spot]
    seq.update(build_sequence(adjacency, path, nucs, start, spot))
    return seq


def build_sequence(adjacency: dict[int, list], path: dict[int, list], nucs: list, start: int, spot: int):
    seq = {}
    if type(adjacency[start][0]) == str:
        return seq
    daughter = build_sequence(adjacency, path, nucs, adjacency[start][0], path[start][spot][0])
    son = build_sequence(adjacency, path, nucs, adjacency[start][1], path[start][spot][1])
    seq.update(daughter)
    seq.update(son)
    seq[adjacency[start][0]] = nucs[path[start][spot][0]]
    seq[adjacency[start][1]] = nucs[path[start][spot][1]]
    return seq


def tree_parsimony(inputs: dict[int, list]):
    sequences = {}
    adjacency = {}
    for i in range(max(inputs.keys())+1):
        sequences[i] = ""
    spot = 0
    for key in inputs:
        if type(inputs[key][0]) == str:
            sequences[spot] = inputs[key][0]
            adjacency[key] = [spot, spot+1]
            spot += 1
            sequences[spot] = inputs[key][1]
            spot += 1
        else:
            adjacency[key] = inputs[key]
    for j in range(len(sequences[0])):
        next_nucs = small_parsimony(j, inputs)
        for key in next_nucs:
            sequences[key] += next_nucs[key]
    #print(sequences)
    #print(adjacency)
    total_distance = 0
    for key in adjacency:
        for item in adjacency[key]:
            first = sequences[key]
            second = sequences[item]
            distance = hamming_distance(first, second)
            total_distance += distance
            print(first + "->" + second + ":" + str(distance))
            print(second + "->" + first + ":" + str(distance))
    print(total_distance)


# adjacency_list = {
#     4: ["CAAATCCC", "ATTGCGAC"],
#     5: ["CTGCGCTG", "ATGGACGA"],
#     6: [4, 5]
# }
# tree_parsimony(adjacency_list)

adj_list = {}
with open('data.txt', 'r') as file:
    for line in file:
        line = line.strip()
        #print(line.strip())
        result = line.split("->")
        if len(result) != 2:
            continue
        #print(result)
        if "A" in result[1] or "C" in result[1]:
            value = result[1]
        else:
            value = int(result[1])
        if int(result[0]) not in adj_list:
            adj_list[int(result[0])] = [value]
        else:
            adj_list[int(result[0])].append(value)

tree_parsimony(adj_list)


import sys
from typing import List, Dict, Tuple
import numpy as np
import random


def parse_tree(filename):

    adjacency_list = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip()) #1st line

    for line in lines[1:]:
        #Split the line at '->' symbol
        node1, node2 = line.strip().split("->")

        if node1 not in adjacency_list:
            adjacency_list[node1] = []
        if node2 not in adjacency_list[node1]:
            adjacency_list[node1].append(node2)
    
        if node2 not in adjacency_list:
            adjacency_list[node2] = []
        if node1 not in adjacency_list[node2]:
            adjacency_list[node2].append(node1)

   
    return n, adjacency_list


def print_adjacency_list(adjacency_list):
    for node, neighbors in adjacency_list.items():
        print(f"{node}: {' '.join(neighbors)}")


def hamming_distance(suffix: str, text: str) -> int:
    # Returns number of mismatches between two strings
    distance = 0
    if len(suffix) > len(text):
        length = len(text)
        distance = len(suffix) - len(text)
    elif len(suffix) < len(text):
        length = len(suffix)
        distance = len(text) - len(suffix)
    else:
        length = len(suffix)

    for i in range(0, length):
        if suffix[i] != text[i]:
            distance += 1
    return distance

def small_parsimony(n: int, adjacency: dict[int, list]) -> dict:
    tags = {}
    s = {}
    nucs = ["A", "C", "G", "T"]
    for node in adjacency:
        tags[node] = 0
        all_str = True
        for item in adjacency[node]:
            if type(item) != str:
                all_str = False
                break
        if all_str:
            tags[node] = 1
            for k in nucs:
                val = 0
                for child in adjacency[node]:
                    if k != child[n]:
                        val += 1
                if node in s:
                    s[node].append(val)
                else:
                    s[node] = [val]
    path = {}
    for key in adjacency:
        if tags[key] == 1:
            continue
        children = []
        for child in adjacency[key]:
            if type(child) == str:
                children.append(child[n])
            else:
                if child in s:
                    children.append(s[child])
        for i in range(len(nucs)):
            min_val = -1
            min_pos = []
            for child in children:
                if type(child) == str:
                    if child != nucs[i]:
                        if min_val == -1:
                            min_val = 1
                        else:
                            min_val += 1
                    else:
                        if min_val == -1:
                            min_val = 0
                    min_pos.append(i)
                else:
                    val = min(child)
                    if child[i] == val:
                        min_val += val
                        min_pos.append(i)
                    else:
                        min_val += val + 1
                        min_pos.append(child.index(val))
            if key not in path:
                path[key] = [min_pos]
            else:
                path[key].append(min_pos)
            if key not in s:
                s[key] = [min_val]
            else:
                s[key].append(min_val)
        tags[key] = 1
    seq = {}
    #print(s.keys())
    #print(s.keys()[:1]) #Get highest number (root is highest number)
    s_2 = list(s.keys())
    highest_node = s_2[-1]
    start = highest_node
    #start = max(s.keys())
    spot = s[start].index(min(s[start]))
    seq[start] = nucs[spot]
    seq.update(build_sequence(adjacency, path, nucs, start, spot, []))
    return seq

def build_sequence(adjacency: dict[int, list], path: dict[int, list], nucs: list, start: int, spot: int, recursion: list):
    seq = {}
    recursion.append(start)
    for val in range(len(path[start][spot])):
        if type(adjacency[start][val]) == str:
            continue
        if adjacency[start][val] in path and adjacency[start][val] not in recursion:
            child = build_sequence(adjacency, path, nucs, adjacency[start][val], path[start][spot][val], recursion)
            seq.update(child)
        seq[adjacency[start][val]] = nucs[path[start][spot][val]]
    return seq

def tree_parsimony(inputs: dict[int, list]):
    sequences = {}
    adjacency = {}
    s_2 = list(inputs.keys())
    highest_node = s_2[-1]
    start = highest_node
    for i in range(start+1):
        sequences[i] = ""
    spot = 0
    for key in inputs:
        if type(inputs[key][0]) == str:
            sequences[spot] = inputs[key][0]
            adjacency[key] = [spot, spot+1]
            spot += 1
            sequences[spot] = inputs[key][1]
            spot += 1
        else:
            adjacency[key] = inputs[key]
    for j in range(len(sequences[0])):
        next_nucs = small_parsimony(j, inputs)
        for key in next_nucs:
            sequences[key] += next_nucs[key]
    #print(sequences)
    #print(adjacency)
    total_distance = 0
    for key in adjacency:
        for item in adjacency[key]:
            print(key)
            print(sequences)
            print(adjacency)
            first = sequences[key] #Accessed by value
            second = sequences[item]
            distance = hamming_distance(first, second)
            total_distance += distance
            print(first + "->" + second + ":" + str(distance))
            print(second + "->" + first + ":" + str(distance))
    print(total_distance)


# adjacency_list = {
#     4: ["CAAATCCC", "ATTGCGAC"],
#     5: ["CTGCGCTG", "ATGGACGA"],
#     6: [4, 5]
# }
# tree_parsimony(adjacency_list)


def parsimony_in_unrooted_tree(adjacency_list: Dict[str, List], n_leaves: int):
    """
    Selects a random edge from the unrooted tree and roots the tree at that edge.
    
    Parameters:
    - adjacency_list: Dict[str, List] representing the tree's adjacency list.
    - n_leaves: int representing the number of leaves in the tree.
    
    Returns:
    - rooted_adjacency: Dict[str, List] representing the rooted tree's adjacency list.
    - root_node: int representing the new root node's identifier.
    """
    edges = []
    seen = set()
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            # (min, max) ordering? 
            edge = tuple(sorted((node, neighbor)))
            if edge not in seen:
                edges.append(edge)
                seen.add(edge)

    if not edges:
        print("The tree has no edges to select.")
        return adjacency_list, None

    # oGetting random edge
    selected_edge = random.choice(edges)
    node1, node2 = selected_edge
    print(f"Selected random edge for rooting the tree: {node1} <-> {node2}")

    numeric_keys = [int(key) for key in adjacency_list.keys() if key.isdigit()]
    if numeric_keys:
        new_root = max(numeric_keys) + 1 #New root number, just +1 to 5
    else:
        new_root = 0 # failsafe
    new_root = str(new_root)
    print(f"New root node created with ID: {new_root}")

    # Removing connection between node1 and node2
    adjacency_list[node1].remove(node2)
    adjacency_list[node2].remove(node1)
    # Adding new root and connecting it to node1 and node2
    adjacency_list[new_root] = [node1, node2]
    adjacency_list[node1].append(new_root)
    adjacency_list[node2].append(new_root)

    print(f"Rooted the tree: Connecting new root {new_root} the the edge between {node1} and {node2}.")
    return adjacency_list, new_root


# When parsing, have separate dictionary that keeps the str vals for each number.
# f more sequences than numbers, need to start +1'ing them to get higher vals
# 
#MAIN: ------------------------------
file = "c:\\Users\\zenit\\BYUSchoolCoding\\Algorithms-BIO-CS-\\Bio364\\Chapter_5\\dataset.txt"
n, adjacency_list = parse_tree(file)
#print("Number of leaves (n):", n)
#print("Adjacency list:")
#print(adjacency_list)
#print_adjacency_list(adjacency_list)

rooted_adjacency, root = parsimony_in_unrooted_tree(adjacency_list, n)

print("\nAdjacency list after rooting:")
print_adjacency_list(rooted_adjacency)
print(f"\nTree has been rooted at node: {root}")

new_adj_list = {}
#Converting all str values into ints:
for key, values in rooted_adjacency.items():
    new_key = int(key) if key.isdigit() else key
    
    new_values = [int(value) if value.isdigit() else value for value in values]
    
    new_adj_list[new_key] = new_values

#print(new_adj_list)
#seq = small_parsimony(n, new_adj_list)
seq2 = tree_parsimony(new_adj_list)
print(seq2)

#Remove the root, turn back into old tree
    #The n value corresponds to the position in the sequence



""" 
adj_list = {}
with open('dataset.txt', 'r') as file:
    for line in file:
        line = line.strip()
        #print(line.strip())
        result = line.split("->")
        if len(result) != 2:
            continue
        #print(result)
        if "A" in result[1] or "C" in result[1]:
            value = result[1]
        else:
            value = int(result[1])
        if int(result[0]) not in adj_list:
            adj_list[int(result[0])] = [value]
        else:
            adj_list[int(result[0])].append(value)
tree_parsimony(adj_list) """


'''
Step ideas?:
    1. Select a random edge and root the tree
    2. Apply small parsimony to the rooted tree
    3. Remove the artificially added root to revert to the unrooted tree
    4. Calculate and return the total parsimony scorem labeled sequences, and the adjacency list
    Input: An integer n followed by an adjacency list for an unrooted binary tree with n leaves labeled by DNA strings.
    Output: The minimum parsimony score of this tree, followed by the adjacency list of the tree corresponding to labeling 
        internal nodes by DNA strings in order to minimize the parsimony score of the tree.
'''