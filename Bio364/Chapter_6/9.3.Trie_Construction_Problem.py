import sys
from typing import List, Dict, Iterable, Tuple, Set

# Please do not remove package declarations because these are used by the autograder.

# Insert your trie_construction function here, along with any subroutines you need
def trie_construction(patterns: List[str]) -> List[Tuple[int, int, str]]:
    """
    Construct a trie from a collection of patterns.
    Input: A space-separated collection of strings Patterns.

    Output: The adjacency list corresponding to Trie(Patterns), in the following format. If Trie(Patterns) has n 
        nodes, first label the root with 0 and then label the remaining nodes with the integers 1 through n - 1 in any 
        order you like. Each edge of the adjacency list of Trie(Patterns) will be encoded by a triple: the first two 
        members of the triple must be the integers labeling the initial and terminal nodes of the edge, respectively; 
        the third member of the triple must be the symbol labeling the edge.
    """
    Trie = {0:{}} #Use dictionaries and then create it as an adj list (at bottom)
    fst_node = 0 
    newNode = 0
    #root node is just 0

    for pattern in patterns:
        currNode = fst_node
        for i in range(len(pattern)):
            currSymbol = pattern[i]
            if currSymbol in Trie[currNode]:
                currNode = Trie[currNode][currSymbol]
            else: #create new node:
                newNode += 1
                Trie[currNode][currSymbol] = newNode
                Trie[newNode] = {}
                currNode = newNode
    #print(Trie)
                
    adjacency_list_trie = [[]]
    for node in Trie:
        for symbol, next_node in Trie[node].items():
            adjacency_list_trie.append((node, next_node, symbol))
    #print(adjacency_list_trie)

    return(adjacency_list_trie)

input = ["ATAGA","ATC","GAT"]
#print(trie_construction(input))