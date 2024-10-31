
import numpy as np
import copy

def hamming(s1,s2):
    assert len(s1) == len(s2)
    d = 0
    for i in range(len(s1)):
        if s1[i]!=s2[i]:
            d+=1
    return d

def small_parsimony_problem(n, edges, labels):
    """
    Small Parsimony Problem. Find the most parsimonious labeling of the internal nodes of a rooted tree. 
    Input: A rooted binary tree with each leaf labeled by a string of length m.
    Output: A labeling of all other nodes of the tree by strings of length m 
    that minimizes the parsimony score of the tree.
    """

    # m, total node count
    m = 2 * n - 1    
    
    # Compute tree and reverse-tree from edges
    tree = {}
    parent = {}
    for edge in edges:
        node = edge[0]
        child = edge[1]
        tree.setdefault(node, []).append(child)
        parent[child] = node

    # Get the root from parent list
    first_key = list(parent.keys())[0]
    root = parent[first_key]
    while root in parent.keys():
        root = parent[root]

    # l, size of string labels
    l = len(labels[0])
    
    # Alphabet of characters of labels
    alphabet = sorted(list(set(''.join(labels))))
    
    # k, number of characters in string labels
    k = len(alphabet)
    
    # d, dictionary of every character position in the alphabet
    d = dict(zip(alphabet, range(k)))

    # Initialize string labels 
    s = [[' ']*l for _ in range(m)]
    
    # Initialize sk matrix
    sk = np.ndarray(shape=(m, k, l), dtype=int)
    
    # Maximum parsimony value is (m-1)*l
    sk.fill((m-1)*l)
    
    # Fill leaf sk according to labels
    for i, label in enumerate(labels):
        s[i] = list(label)
        for j, c in enumerate(label):
            sk[i, d[c], j] = 0
    
    # Depth-first search for each string element to fill sk values
    for i in range(l):
        def dfs_sk(node):
            if node < n:
                # Leaf node; already processed
                return
            lnode, rnode = tree[node]
            dfs_sk(lnode)
            dfs_sk(rnode)
            for j in range(k):
                mask = np.ones(k)
                mask[j] = 0
                # Ensure integer type for addition
                sk[node, j, i] = min(sk[lnode, :, i] + mask.astype(int)) + min(sk[rnode, :, i] + mask.astype(int))
        dfs_sk(root)
    
    # Calculate parsimony score
    parsimony = sum(sk[root].min(axis=0))
    
    # Depth-first search to back propagate the internal node string s values 
    for i in range(l):        
        def dfs_s(node):
            if node < n:
                # Leaf node
                return
            c = sk[node, :, i]
            if node == root:
                # When root, choose the symbol with minimum score
                s[node][i] = alphabet[c.argmin()]
            else:
                pnode = parent[node]
                j = d[s[pnode][i]]
                mask = np.ones(k)
                mask[j] = 0
                mask = mask.astype(int)
                c += mask
                s[node][i] = alphabet[c.argmin()]
            
            lnode, rnode = tree[node]
            dfs_s(lnode)
            dfs_s(rnode)
        dfs_s(root)
    
    # Compile the list of edges with labels
    ret = []
    for node, (lnode, rnode) in tree.items():
        ps = ''.join(s[node])
        ls = ''.join(s[lnode])
        rs = ''.join(s[rnode])
        ret.append((ps, ls))
        ret.append((ps, rs))
    
    # Return only the parsimony score and the list of edges
    return (parsimony, ret[:])


def small_parsimony_unrooted_problem(n,uedges,labels):
    '''
    CODE CHALLENGE: Solve the Small Parsimony in an Unrooted Tree Problem.
    Input: An integer n followed by an adjacency list for an unrooted binary tree with n leaves
    labeled by DNA strings.
    Output: The minimum parsimony score of this tree, followed by the adjacency list of the
    tree corresponding to labeling internal nodes by DNA strings in order to minimize the
    parsimony score of the tree.
    '''
    # compute unrooted tree from edges
    utree = {}
    m = n+1
    for uedge in uedges:
        node = uedge[0]
        child = uedge[1]
        m = max(node+1,child+1,m)
        utree.setdefault(node,[]).append(child)
    
    # m, total node count
    
     # given edge create a rooted tree from unrooted tree
    def get_rooted_tree(uedge):
        (lnode,rnode) = uedge
        root = m
        visited = [False]*(m+1)
        edges = []
        rooted_tree = copy.deepcopy(utree)
        rooted_tree[rnode].remove(lnode)
        rooted_tree[lnode].remove(rnode)
        rooted_tree[root] = [lnode,rnode]
        def dfs_rooted_tree(node):
            if (node < n) or (visited[node] == True):
                # tree bottom or already visited, simply return
                return
            visited[node] = True
            for child in rooted_tree[node]:
                if (visited[child] == False ):
                    edges.append((node,child))
                    dfs_rooted_tree(child)
            return
        dfs_rooted_tree(root)      
        return edges

    perls = []
    for uedge in set([(min(a,b),max(a,b)) for (a,b) in uedges]):
        edges = get_rooted_tree(uedge)
        perl = small_parsimony_problem(n,edges,labels)
        perls.append(perl)
    (p,e,r,l) = min(perls)
    # find root's children
    ret = [(edge[0],edge[1]) for edge in e if (edge != r and edge !=l)]
    ret.append((l[1],r[1]))
    return (p,ret)


def edge2tree(edges):
    tree = {}
    for e in edges:
        node = e[0]
        child = e[1]
        tree.setdefault(node,[]).append(child)
    return tree
    
def tree2edge(tree):
    edges = []
    for node,children in tree.items():
        for child in children:
            edges.append((node,child))
    return edges

def tree_nearest_neighbors(e,utree):
    '''
    CODE CHALLENGE: Solve the Nearest Neighbors of a Tree Problem.
    Input: Two internal nodes a and b specifying an edge e, followed by an adjacency
    list of an unrooted binary tree.
    Output: Two adjacency lists representing the nearest neighbors of the tree with
    respect to e. Separate the adjacency lists with a blank line.
    '''
    a = e[0]
    b = e[1]
    
    atree = utree[a][:]
    atree.remove(b)
    w = atree[0]
    x = atree[1]
    btree = utree[b][:]
    btree.remove(a)
    y = btree[0]
    z = btree[1] 

#    # neighbor utree1 is like wya <=>bxz :
#    utree1 = copy.copy(utree)
#    utree1[a] = [b,y,w]
#    utree1[y] = utree1[y][:]
#    utree1[y].remove(b)
#    utree1[y].append(a)
#    utree1[b] = [a,x,z]
#    utree1[x] = utree1[x][:]
#    utree1[x].remove(a)
#    utree1[x].append(b)
#        
#    # neighbor utree2 is like wza <=>bxy :
#    utree2 = copy.copy(utree)
#    utree2[a] = [b,z,w]
#    utree2[z] = utree2[z][:]
#    utree2[z].remove(b)
#    utree2[z].append(a)
#    utree2[b] = [a,x,y]
#    utree2[x] = utree2[x][:]
#    utree2[x].remove(a)
#    utree2[x].append(b)
#    return (utree1,utree2)
    
    # neighbor utree1 is like wya <=>bxz :
    utree1 = copy.deepcopy(utree)
    utree1[a] = [b,y,w]
    utree1[y].remove(b)
    utree1[y].append(a)
    utree1[b] = [a,x,z]
    utree1[x].remove(a)
    utree1[x].append(b)
        
    # neighbor utree2 is like wza <=>bxy :
    utree2 = copy.deepcopy(utree)
    utree2[a] = [b,z,w]
    utree2[z].remove(b)
    utree2[z].append(a)
    utree2[b] = [a,x,y]
    utree2[x].remove(a)
    utree2[x].append(b)
    return (utree1,utree2)

            
def parsing_large_parsimony_problem_input(lines):
    n = int(lines[0])
    labels = []
    edges = []
    for l in lines[1:]:
        a = l.split('->')[0]
        b = l.split('->')[1]
        if a.isdigit() == True:
            a = int(a)
        else:
            if a not in labels:
                labels.append(a)
            a = labels.index(a)
        if b.isdigit() == True:
            b = int(b)
        else:
            if b not in labels:
                labels.append(b)
            b = labels.index(b)
        edges.append((a,b))
    return n,edges,labels


############################################################
fpath = 'C:/Users/zenit/BYUSchoolCoding/Algorithms-BIO-CS-/Bio364/Chapter_5/'
#fpath = '/home/ngaude/Downloads/'
#fpath = 'C:/Users/Utilisateur/Downloads/'
############################################################

fname = fpath + 'dataset.txt'

with open(fname, "r") as f:
    lines = f.read().strip().split('\n')
    n = int(lines[0])
    
    # Extract labels for the first n lines (assuming they are in the format "id->label")
    labels = [line.split('->')[1] for line in lines[1:n+1]]
    
    # Process the first n lines to create parent-child relationships for leaves
    v = [(int(line.split('->')[0]), i) for i, line in enumerate(lines[1:n+1])]
    
    # Process the remaining lines to create parent-child relationships for internal nodes
    internal_edges = [(int(line.split('->')[0]), int(line.split('->')[1])) for line in lines[n+1:]]
    
    # Combine all edges
    v += internal_edges
    
    # Call the Small Parsimony Problem function with updated unpacking
    p, e = small_parsimony_problem(n, v, labels)

# Write the output to a file
with open(fname + '.out', "w") as f:
    f.write(f"{p}\n")
    for a, b in e:
        distance = hamming(a, b)
        f.write(f"{a}->{b}:{distance}\n")
        f.write(f"{b}->{a}:{distance}\n")

#fname = fpath + 'Small_Parsimony_Unrooted_Tree.txt'
#fname = fpath + 'dataset_10335_12.txt'
#with open(fname, "r") as f:
#    lines = f.read().strip().split('\n')
#    n = int(lines[0])
#    labels = map(lambda l:l.split('->')[0],lines[1:2*n+1:2])
#    v  = map(lambda (i,l):(i,int(l.split('->')[1])),enumerate(lines[1:2*n+1:2]))
#    v += map(lambda (i,l):(int(l.split('->')[0]),i),enumerate(lines[2:2*n+1:2]))
#    v += map(lambda l:(int(l.split('->')[0]),int(l.split('->')[1])),lines[2*n+1:])
#    (p,e) = small_parsimony_unrooted_problem(n,v,labels)
#with open(fname+'.out', "w") as f:
#    f.write(str(p)+'\n')
#    for (a,b) in e:
#        f.write(a+'->'+b+':'+str(hamming(a,b))+'\n')
#        f.write(b+'->'+a+':'+str(hamming(a,b))+'\n')

#fname = fpath + 'dataset_10336_6.txt'
#with open(fname, "r") as f:
#    lines = f.read().strip().split('\n')
#    a = int(lines[0].split(' ')[0])
#    b = int(lines[0].split(' ')[1])
#    v = map(lambda l:(int(l.split('->')[0]),int(l.split('->')[1])),lines[1:])
#edge1,edge2 = map(tree2edge, tree_nearest_neighbors((a,b), edge2tree(v)))
#s = '\n'.join(map(lambda e: str(e[0])+'->'+str(e[1]),edge1))
#s += '\n'+'\n'
#s += '\n'.join(map(lambda e: str(e[0])+'->'+str(e[1]),edge2))
#with open(fname+'.out', "w") as f:
#    f.write(s)

""" fname = fpath + 'dataset.txt'
#fname = fpath + 'Large_Parsimony_Heuristic_with_NNI.txt'
with open(fname, "r") as f:
    lines = f.read().strip().split('\n')
    n,edges,labels = parsing_large_parsimony_problem_input(lines)
pes = large_parsimony_problem(n,edges,labels)
with open(fname+'.out', "w") as f:
    for p,e in pes:
        f.write(str(p)+'\n')
        for (a,b) in e:
            f.write(a+'->'+b+':'+str(hamming(a,b))+'\n')
            f.write(b+'->'+a+':'+str(hamming(a,b))+'\n') """