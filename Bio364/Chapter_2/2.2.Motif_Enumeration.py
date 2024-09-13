import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your motif_enumeration function here, along with any subroutines you need
def motif_enumeration(dna: list[str], k: int, d: int) -> list[str]:
    """Implements the MotifEnumeration algorithm."""
    Patterns = []

    #for each k-long pattern in mer...:
        #
    
    for mer in dna:
        all_neighbors = neighbors(mer, d)
        for mer2 in all_neighbors:
            if mer2 in 

        #for each k-mer Pattern’ differing from Pattern by at most d mismatches
        #    if Pattern' appears in each string from Dna with at most d mismatches
        #        add Pattern' to Patterns
    #remove duplicates from Patterns

    pass


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


k = 3
d = 1
dna = ["ATTTGGC", "TGCCTTA", "CGGTATC", "GAAAATT"]
print(motif_enumeration(dna, k, 3))