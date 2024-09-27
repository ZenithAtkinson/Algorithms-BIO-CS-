import sys
from typing import List, Dict, Iterable

# Please do not remove package declarations because these are used by the autograder.

# Insert your eulerian_cycle function here, along with any subroutines you need
# g[u] is the list of neighbors of the vertex u
def eulerian_path(g: Dict[int, List[int]]) -> Iterable[int]:
    """Constructs an Eulerian pathe in a graph."""
    new_path = []
    start = get_start(g)
    end = get_end(g)
    if start != -1:
        if end in g.keys():
            g[end].append(start)
        else:
            g[end] = [start]


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
    for p in range(len(new_path)-1):
        if new_path[p] == end and new_path[p+1] == start:
            break
        
    new_path2 = new_path[p:]
    new_path2.extend(new_path[1:p+1])
    new_path = new_path2
    new_path = new_path[1:]

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

def get_start(g: Dict[int, List[int]]):
    for i in g:
        count = 0
        for j in g:
            for k in g[j]:
                if k == i:
                    count+=1
        if (count < len(g[i])):
            return i
    return -1

def get_end(g: Dict[int, List[int]]):
    for val in g.values():
        for item in val:
            if item not in g.keys():
                return item
    for i in g:
        count = 0
        for j in g:
            for k in g[j]:
                if k == i:
                    count+=1
        if (count > len(g[i])):
            return i
    return -1
