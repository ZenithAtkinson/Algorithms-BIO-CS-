import sys
from typing import List, Dict, Iterable

# Please do not remove package declarations because these are used by the autograder.

# Insert your kmer_composition function here, along with any subroutines you need
def kmer_composition(text: str, k: int) -> Iterable[str]:
    """Forms the k-mer composition of a string."""
    #Given the text... find all kmers of given length k and return them as a list.
    kmers = []
    kmer = ""
    for c in range(len(text)-(k-1)):
        kmer = text[c:c+k]
        kmers.append(kmer)
    return kmers

input = "CAATCCAAC"
k = 5
#print(kmer_composition(input, k))