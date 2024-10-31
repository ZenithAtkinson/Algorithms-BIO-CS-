import sys
import queue
import numpy as np
from copy import deepcopy

def char_ind_conversion():
    char2ind = {'A':0, 'C':1, 'G':2, 'T':3}
    ind2char = {0:'A', 1:'C', 2:'G', 3:'T'}
    return char2ind, ind2char

def read_from_file():
    f = open('dataset.txt', 'r')
    data = []
    for line in f:
        data.append(line.strip())
    n = int(data[0])
    adj = [dict() for _ in range(n)]
    nodes = ['' for _ in range(n)]
    curr_node = 0
    for d in data[1:]:
        d = d.split('->')
        try:
            p = int(d[0])
        except:
            p = curr_node
            nodes[p] = d[0]
            curr_node += 1
        try:
            c = int(d[1])
        except:
            continue
        if p > len(adj)-1 or c > len(adj)-1:
            adj.extend([dict() for _ in range(max([p,c])-len(adj)+1)])
        adj[p][c] = 0
        adj[c][p] = 0
    nodes.extend(['' for _ in range(len(adj)-n+1)])
    lastEdge = [int(i) for i in data[-1].split('->')]
    f.close()
    return n, adj, nodes, lastEdge

def save_trees(trees):
    f = open('result.txt', 'w')
    for s, adj, nodes in trees:
        f.write(str(s)+'\n')
        for i, d in enumerate(adj):
            for j, w in d.items():
                f.write(nodes[i]+'->'+nodes[j]+':'+str(w)+'\n')
        f.write('\n')
    f.close()

def print_trees(trees):
    for s, adj, nodes in trees:
        print(s)
        for i, d in enumerate(adj):
            for j, w in d.items():
                print(f"{nodes[i]}->{nodes[j]}:{w}")
        print('')

def single_small_parsimony(n, adjC, adjP, adj, nodes, char2ind, ind2char, charInd):
    s = [[np.inf]*4 for _ in range(len(adjC))]
    backtrack = [[(-1, -1) for _ in range(4)] for __ in range(len(adjC))]
    processed = [0 for _ in range(len(adjC))]
    ripe = set()
    
    # Initialize leaves
    for i in range(n):
        s[i][char2ind[nodes[i][charInd]]] = 0
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

    ind = np.argmin(s[v])
    nodes[v] += ind2char[ind]
    smin = s[v][ind]

    # Backtrack
    q = queue.Queue()
    q.put((v, ind))
    while not q.empty():
        v, k = q.get()
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
                nodes[u] += ind2char[l]
                q.put((u, l))
            if len(adjC[w]) > 0:
                nodes[w] += ind2char[r]
                q.put((w, r))
    
    return smin

def run_small_parsimony(n, adj, nodes, lastEdge):
    def dist(v, w):
        return sum(1 for i in range(len(v)) if v[i] != w[i])

    char2ind, ind2char = char_ind_conversion()
    root = len(adj)
    
    # Modify adjacency list
    del adj[lastEdge[0]][lastEdge[1]]
    del adj[lastEdge[1]][lastEdge[0]]
    adj.append(dict())
    adj[root][lastEdge[0]] = 0
    adj[lastEdge[0]][root] = 0
    adj[root][lastEdge[1]] = 0
    adj[lastEdge[1]][root] = 0
    
    # Create child and parent adjacency lists
    adjC = [[] for _ in range(len(adj))]
    adjP = [[] for _ in range(len(adj))]
    q = queue.Queue()
    q.put(root)
    visited = [False for _ in range(len(adj))]
    visited[root] = True
    
    while not q.empty():
        curr = q.get()
        for v in adj[curr].keys():
            if not visited[v]:
                adjP[v].append(curr)
                visited[v] = True
                q.put(v)
                
    for u, d in enumerate(adjP):
        for v in d:
            adjC[v].append(u)
    
    # Calculate parsimony score
    s = 0
    for i in range(len(nodes[0])):
        s += single_small_parsimony(n, adjC, adjP, adj, nodes, char2ind, ind2char, i)
    
    # Restore adjacency list
    d = dist(nodes[lastEdge[0]], nodes[lastEdge[1]])
    del adj[root]
    del adj[lastEdge[0]][root]
    del adj[lastEdge[1]][root]
    adj[lastEdge[0]][lastEdge[1]] = d
    adj[lastEdge[1]][lastEdge[0]] = d
    
    return s, adj, nodes

def find_nearest_neighbors(edge, adj):
    adj1 = deepcopy(adj)
    adj2 = deepcopy(adj)

    del adj1[edge[0]][edge[1]]
    del adj1[edge[1]][edge[0]]
    e0 = list(adj1[edge[0]].keys())
    e1 = list(adj1[edge[1]].keys())
    
    # First neighbor
    adj1[edge[0]][e1[0]] = 0
    adj1[edge[1]][e0[0]] = 0
    adj1[e1[0]][edge[0]] = 0
    adj1[e0[0]][edge[1]] = 0
    del adj1[e1[0]][edge[1]]
    del adj1[e0[0]][edge[0]]
    del adj1[edge[0]][e0[0]]
    del adj1[edge[1]][e1[0]]
    adj1[edge[0]][edge[1]] = 0
    adj1[edge[1]][edge[0]] = 0

    # Second neighbor
    adj2[edge[0]][e1[1]] = 0
    adj2[edge[1]][e0[0]] = 0
    adj2[e1[1]][edge[0]] = 0
    adj2[e0[0]][edge[1]] = 0
    del adj2[e1[1]][edge[1]]
    del adj2[e0[0]][edge[0]]
    del adj2[edge[0]][e0[0]]
    del adj2[edge[1]][e1[1]]
    
    return adj1, adj2

def run_nearest_neighbor_interchange(n, adj, nodes, lastEdge):
    trees = []
    score = np.inf
    newScore, newAdj, newNodes = run_small_parsimony(n, adj, deepcopy(nodes), lastEdge)
    
    while newScore < score:
        score = newScore
        adj = newAdj
        visited = set()
        
        for v in range(n, len(adj)):
            for u in adj[v].keys():
                if u >= n and (v, u) not in visited:
                    adj1, adj2 = find_nearest_neighbors([v, u], adj)
                    
                    # Process first neighbor
                    for i, a in enumerate(adj1):
                        adj1[i] = dict.fromkeys(a, 0)
                    neighborScore, neighborAdj, neighborNodes = run_small_parsimony(n, adj1, deepcopy(nodes), [v, u])
                    if neighborScore < newScore:
                        newScore = neighborScore
                        newAdj = neighborAdj
                        newNodes = neighborNodes
                    
                    # Process second neighbor
                    for i, a in enumerate(adj2):
                        adj2[i] = dict.fromkeys(a, 0)
                    neighborScore, neighborAdj, neighborNodes = run_small_parsimony(n, adj2, deepcopy(nodes), [v, u])
                    if neighborScore < newScore:
                        newScore = neighborScore
                        newAdj = neighborAdj
                        newNodes = neighborNodes
                    
                    visited.add((v, u))
                    visited.add((u, v))
        
        if newScore < score:
            trees.append((newScore, newAdj, newNodes))
    
    return trees

def main():
    n, adj, nodes, lastEdge = read_from_file()
    trees = run_nearest_neighbor_interchange(n, adj, nodes, lastEdge)
    save_trees(trees)
    print_trees(trees)

if __name__ == "__main__":
    main()