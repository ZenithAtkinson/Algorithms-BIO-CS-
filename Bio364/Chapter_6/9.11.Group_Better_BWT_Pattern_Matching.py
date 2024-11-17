import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your better_bw_matching function here, along with any subroutines you need
def better_bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    """
    Perform an optimized Burrows-Wheeler Matching for a set of patterns against the Burrows-Wheeler Transform of a text.
    """
    
    pass

# Sample input:
# GGCGCCGC$TAGTCACACACGCCGTA
# ACC CCG CAG

# Sample output:
# 1 2 1

'''
BetterBWMatching(FirstOccurrence, LastColumn, Pattern, Count)
    top ← 0
    bottom ← |LastColumn| − 1
    while top ≤ bottom
        if Pattern is nonempty
            symbol ← last letter in Pattern
            remove last letter from Pattern
            if positions from top to bottom in LastColumn contain an occurrence of symbol
                top ← FirstOccurrence(symbol) + Countsymbol(top, LastColumn)
                bottom ← FirstOccurrence(symbol) + Countsymbol(bottom + 1, LastColumn) − 1
            else
                return 0
        else
            return bottom − top + 1
'''