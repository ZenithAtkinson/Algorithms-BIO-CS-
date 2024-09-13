import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your greedy_motif_search function here, along with any subroutines you need
def greedy_motif_search(dna: list[str], k: int, t: int) -> list[str]:
    """Implements the GreedyMotifSearch algorithm."""

    pass


def profile(motif: list[str]):
    size = len(motif[0])
    length = len(motif)
    profile = []
    #count each nuc in each column
    for i in range(0, size):
        chars = {'A':0, 'C':0, 'G':0, 'T':0}
        for j in range(0, len(motif)):
            chars[motif[j][i]] += 1
        profile.append(chars)
        #divide that by the number of rows
        for key in chars:
            val = round(chars[keu]/length, 1)
            chars.update({key: val})
    return profile
            
            
input = ["ACTGGTCAAA"]

profile(input)