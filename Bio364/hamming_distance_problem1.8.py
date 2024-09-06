import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your hamming_distance function here, along with any subroutines you need
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

pat1 = "GGGCCGTTGGT"
pat2 = "GGACCGTTGAC"

print(hamming_distance(pat1, pat2))