import sys
from typing import List, Dict, Iterable

# Please do not remove package declarations because these are used by the autograder.
def string_reconstruction(patterns: List[str], k: int) -> str:
    """Reconstructs a string from its k-mer composition."""
    dB = {}
    dB = de_bruijn_string(patterns, k)
    path = eulerian_path(dB)

    final = ""
    first = True
    #print(path)
    for i in path:
        if first:
            final+=i
            first = False
        else:
            final+= i[-1]
            #print(i[-1])
    
    #final = ""
    #for i in path:
    #    final+=(i[0])
    #
    #final_char = path[-1]
    #final+= (final_char[-1])

    return final


# Insert your de_bruijn_string function here, along with any subroutines you need
def de_bruijn_string(kmers: List[str], k: int) -> Dict[str, List[str]]:
    """Forms the de Bruijn graph of a string."""
    #find all the kmers,
    kmer_dict = {}

    #print(get_prefixes(kmers))
    #print(get_suffixes(kmers))
    k_prefixes = get_prefixes(kmers, k)
    k_suffixes = get_suffixes(kmers, k)
    # #and their prefixes/suffixes.
    #for each prefix, append it to a dictionary and add the suffixes as the key value

    for i in range(len(kmers)):
        if k_prefixes[i] not in kmer_dict:
            kmer_dict[ k_prefixes[i]] = []
        kmer_dict[k_prefixes[i]].append(k_suffixes[i])
    #print(kmer_dict)

    #for key, value in kmer_dict.items():
    #    print(f"{key}: {value}")

    #return dictionary list
    return kmer_dict

def kmer_composition(text: str, k: int) -> Iterable[str]:
    """Forms the k-mer composition of a string."""
    #Given the text... find all kmers of given length k and return them as a list.
    kmers = []
    kmer = ""
    for c in range(len(text)-(k-1)):
        kmer = text[c:c+k]
        kmers.append(kmer)
    return kmers

def get_prefixes(kmer_list: list[str], k: int):
    prefixes = []
    for i in range(len(kmer_list)):
        kmer = kmer_list[i]
        prefixes.append(kmer[0:(k-1)]) #[0:2]
    #return a list of prefixes
    return prefixes

def get_suffixes(kmer_list: list[str], k: int):
    suffixes = []
    for i in range(len(kmer_list)): 
        kmer = kmer_list[i]
        suffixes.append(kmer[1:k]) #[1:3]
    #return a list of prefixes
    return suffixes

# Please do not remove package declarations because these are used by the autograder.

# Insert your eulerian_cycle function here, along with any subroutines you need
# g[u] is the list of neighbors of the vertex u
def eulerian_path(g: Dict[str, List[str]]) -> Iterable[str]:
    """Constructs an Eulerian pathe in a graph."""
    new_path = []
    start = get_start(g)
    end = get_end(g)
    if start != "NULL":
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
        
    if start != "NULL" or end != "NULL":
        for p in range(len(new_path)-1):
            if new_path[p] == end and new_path[p+1] == start:
                break        
        new_path2 = new_path[p:]
        new_path2.extend(new_path[1:p+1])
        new_path = new_path2
        new_path = new_path[1:]

    return new_path

def cycle_checker(g: Dict[str, List[str]], new_path: list, key: str):
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

def get_start(g: Dict[str, List[str]]):
    for i in g:
        count = 0
        for j in g:
            for k in g[j]:
                if k == i:
                    count+=1
        if (count < len(g[i])):
            return i
    return "NULL"

def get_end(g: Dict[str, List[str]]):
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
    return "NULL"

input_text = ["ACG", "CGT", "GTA", "TAC"]
k = 3
#print(string_reconstruction(input_text, k))
