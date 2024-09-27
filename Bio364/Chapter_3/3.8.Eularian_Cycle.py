import sys
from typing import List, Dict, Iterable

# Please do not remove package declarations because these are used by the autograder.

# Insert your eulerian_cycle function here, along with any subroutines you need
# g[u] is the list of neighbors of the vertex u
def eulerian_cycle(g: Dict[int, List[int]]) -> Iterable[int]:
    """Constructs an Eulerian cycle in a graph."""
    new_path = []

    key = list(g.keys())[0]
    #print(key)
    new_path.append(key)
    done = cycle_checker(g, new_path, key)
    while not done:
        i = 0
        #print("test")
        while i < (len(new_path)):
            if len(g[new_path[i]]) > 0:
                key = new_path[i]
                #print("key : ",key)
                break
            i += 1
        new_path2 = new_path[i:]
        new_path2.extend(new_path[1:i+1])
        new_path = new_path2
        done = cycle_checker(g, new_path, key)
    
    #print(g)
    return new_path

def cycle_checker(g: Dict[int, List[int]], new_path: list, key: int):
    #Each time you move along the edge, take that given value out of the dictionary list.
        #Add it to a straight list which is the path.
    running = True
    while running:
        #Cut out each key, when it is empty
        #edge = key[0]
        edge = g[key].pop(0)
        key = edge
        new_path.append(edge)
        #print(g)
        #print(new_path)

        if (len(g[edge])==0):
            running == False
            break
    for i in g:
        if len(g[i]) >= 1:
            #print("its not finished")
            return False
        
    return True
    
