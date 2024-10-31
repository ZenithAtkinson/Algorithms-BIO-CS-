import sys
import numpy as np
from copy import deepcopy

def parse_input():
    data = sys.stdin.read().strip().split('\n')
    n = int(data[0]) #1st val = n

    adj = []
    for i in range(n):
        adj.append({}) 
    nodes = []
    for index in range(n):
        nodes.append('')

    currNode = 0
    #c, p: child, parent
    for d in data[1:]:
        d = d.split('->') #like bfore, splitting by ->
        try:
            p = int(d[0])
        except:
            p = currNode
            nodes[p] = d[0]
            currNode += 1
        try:
            c = int(d[1])
        except:
            continue
        if p > len(adj)-1 or c > len(adj)-1:
            highest_node_index = max(p, c)
            # number of new adjacency dictionaries need to be added:
            required_length = highest_node_index - len(adj) + 1
            if required_length > 0:
                for node_number in range(required_length):
                    adj.append({})
        adj[p][c] = 0
        adj[c][p] = 0

    additional_nodes_needed = len(adj) - n + 1

    # Addign EMPTY strings
    for i in range(additional_nodes_needed):
        nodes.append('')

    lastEdge = [int(i) for i in data[-1].split('->')]
    return n, adj, nodes, lastEdge

#Char conversions for 2 dictionaries for outputting / accessing correct indicies (needs to be by number)
def get_char_conversions():
    char2int = {'A':0, 'C':1, 'G':2, 'T':3}
    int2char = {0:'A', 1:'C', 2:'G', 3:'T'}
    return char2int, int2char

def small_parsimony(n, adjC, adjP, adj, nodes, char2int, int2char, charInd):
    s = [[np.inf]*4 for _ in range(len(adjC))]
    backtrack = [[(-1, -1) for _ in range(4)] for __ in range(len(adjC))]
    processed = [0 for _ in range(len(adjC))]
    ripe = set()
    
    # Initialize leaf nodes
    for i in range(n):
        s[i][char2int[nodes[i][charInd]]] = 0
        processed[i] = 1
        if len(adjP[i]) > 0:
            ripe.add(adjP[i][0])
    
    # Process internal nodes
    while len(ripe) > 0:
        v = ripe.pop()
        for k in range(4):
            l = [s[adjC[v][0]][i] + (0 if k == i else 1) for i in range(4)]
            r = [s[adjC[v][1]][i] + (0 if k == i else 1) for i in range(4)]
            largmin = np.argmin(l)
            rargmin = np.argmin(r)
            backtrack[v][k] = (largmin, rargmin)
            s[v][k] = l[largmin] + r[rargmin]
        processed[v] = 1
        if len(adjP[v]) > 0 and all([processed[u] for u in adjC[adjP[v][0]]]):
            ripe.add(adjP[v][0])
    
    # Backtrack to assign characters
    ind = np.argmin(s[v])
    nodes[v] += int2char[ind]
    smin = s[v][ind]

    # Use list as queue
    process_list = [(v, ind)]
    while process_list:
        v, k = process_list.pop(0)  # Pop from beginning of list (queue-like behavior)
        if len(adjC[v]) > 0:
            u, w = adjC[v]
            l, r = backtrack[v][k]
            
            if k != l:
                adj[v][u] += 1
                adj[u][v] += 1
            if k != r:
                adj[v][w] += 1
                adj[w][v] += 1
            if len(adjC[u]) > 0:
                nodes[u] += int2char[l]
                nodes[w] += int2char[r]
                process_list.append((u, l))
                process_list.append((w, r))        
    return smin

def calculate_distance(v, w):
    d = 0
    l = len(v)
    for i in range(l):
        if v[i] != w[i]:
            d += 1
    return d

def run_small_parsimony(n, adj, nodes, lastEdge):
    char2int, int2char = get_char_conversions()
    
    # Add root node
    root = len(adj)
    del adj[lastEdge[0]][lastEdge[1]]
    del adj[lastEdge[1]][lastEdge[0]]
    adj.append(dict())
    adj[root][lastEdge[0]] = 0
    adj[lastEdge[0]][root] = 0
    adj[root][lastEdge[1]] = 0
    adj[lastEdge[1]][root] = 0
    
    # Create adjacency lists
    adjC = [[] for _ in range(len(adj))]
    adjP = [[] for _ in range(len(adj))]
    for p in range(n, len(adj)):
        c = sorted(list(adj[p].keys()))
        adjC[p].append(c[0])
        adjC[p].append(c[1])
        adjP[c[0]].append(p)
        adjP[c[1]].append(p)
    
    # Calculate parsimony score
    s = 0
    for i in range(len(nodes[0])):
        s += small_parsimony(n, adjC, adjP, adj, nodes, char2int, int2char, i)
    
    # Clean up and restore original edge
    d = calculate_distance(nodes[lastEdge[0]], nodes[lastEdge[1]])
    del adj[root]
    del adj[lastEdge[0]][root]
    del adj[lastEdge[1]][root]
    adj[lastEdge[0]][lastEdge[1]] = d
    adj[lastEdge[1]][lastEdge[0]] = d
    
    return s

def print_results(s, adj, nodes):
    print(s)
    for i, d in enumerate(adj):
        for j, w in d.items():
            print(nodes[i]+'->'+nodes[j]+':'+str(w))

def main():
    n, adj, nodes, lastEdge = parse_input()
    s = run_small_parsimony(n, adj, nodes, lastEdge)
    print_results(s, adj, nodes)

if __name__ == "__main__":
    main()


""" rooted_adjacency, root = parsimony_in_unrooted_tree(adjacency_list, n)
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
print(seq2) """

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