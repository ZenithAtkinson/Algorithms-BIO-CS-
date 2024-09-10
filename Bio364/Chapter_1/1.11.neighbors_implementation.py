import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your neighbors function here, along with any subroutines you need
def neighbors(s: str, d: int) -> list[str]:
    """Generate neighbors of a string within a given Hamming distance."""
    if d == 0:
        return [s]
    if len(s) == 1:
        return ['A', 'C', 'G', 'T']
    neighborhood = []
    suffixNeighbors = neighbors(Suffix(s), d)
        #What is suffix? What does it mean?
        #I think that Suffix(pattern) is the pattern without its first value (so ACT would just be CT)
    #print(suffixNeighbors)
    for text in suffixNeighbors:
        if hamming_distance(Suffix(s), text) < d:
            for x in {"A", "C", "G", "T"}:
                neighborhood.append(x+text)
            #print(text)
        else:
            neighborhood.append(s[0]+text)
    return neighborhood

def Suffix(s: str):
    s_len = len(s)
    new_s = s[1:s_len]
    return new_s

def hamming_distance(p: str, q: str) -> int:
    """Calculate the Hamming distance between two strings."""
    #for each mismatche between two strings, add 1 to the hamming distance. a hamming distance of 0 is a perfect match.
    ham = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            #print(p[i])
            #print(q[i])
            ham += 1
    return ham

#pattern = "CGATGGCCTA"

s = "ACG"
d = 1

#print(neighbors(s, d))
