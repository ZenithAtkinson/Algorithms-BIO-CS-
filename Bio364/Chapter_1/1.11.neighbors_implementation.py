import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your neighbors function here, along with any subroutines you need
def neighbors(s: str, d: int) -> list[str]:
    """Generate neighbors of a string within a given Hamming distance."""
    if d == 0:
        return(s)
    if len(s) == 1:
        return {'A', 'C', 'G', 'T'}
    neighborhood = []
    suffixNeighbors = neighbors(Suffix(s)m d)
        #What is suffix? What does it mean?


    pass