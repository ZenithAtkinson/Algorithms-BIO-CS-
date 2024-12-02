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
    with open("output.txt", "w") as output_file:  # Open output.txt for writing
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
        total_distance = 0
        for key in adjacency:
            for item in adjacency[key]:
                first = sequences[key]
                second = sequences[item]
                distance = hamming_distance(first, second)
                total_distance += distance
                line1 = f"{first}->{second}:{distance}"
                line2 = f"{second}->{first}:{distance}"
                print(line1)
                print(line2)
                output_file.write(line1 + "\n")
                output_file.write(line2 + "\n")
        print(total_distance)
        output_file.write(f"{total_distance}\n")


# adjacency_list = {
#     4: ["CAAATCCC", "ATTGCGAC"],
#     5: ["CTGCGCTG", "ATGGACGA"],
#     6: [4, 5]
# }
# tree_parsimony(adjacency_list)

adj_list = {}
with open('input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        result = line.split("->")
        if len(result) != 2:
            continue
        if "A" in result[1]:
            value = result[1]
        else:
            value = int(result[1])
        if int(result[0]) not in adj_list:
            adj_list[int(result[0])] = [value]
        else:
            adj_list[int(result[0])].append(value)
tree_parsimony(adj_list)