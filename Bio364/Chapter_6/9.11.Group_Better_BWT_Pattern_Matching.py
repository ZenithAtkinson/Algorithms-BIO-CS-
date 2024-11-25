import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your better_bw_matching function here, along with any subroutines you need
def better_bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    """
    Perform an optimized Burrows-Wheeler Matching for a set of patterns against the Burrows-Wheeler Transform of a text.
    """
    first_column = sorted(bwt)
    last_column = list(bwt)

    first_occurrence_map = first_occurance(first_column)
    countsymbol_map = counted_symbols(last_column)

    result = []

    for pattern in patterns:
        top = 0
        bottom = len(bwt) - 1
        current_pattern = pattern
        found = True

        while top <= bottom and len(current_pattern) > 0:
            #print(current_pattern)
            symbol = current_pattern[-1]
            current_pattern = current_pattern[:-1]
            '''top ← FirstOccurrence(symbol) + Countsymbol(top, LastColumn)
            bottom ← FirstOccurrence(symbol) + Countsymbol(bottom + 1, LastColumn) - 1'''
            if symbol in first_occurrence_map:
                #print(symbol)
                count_top = countsymbol_map[symbol][top - 1] if top > 0 else 0

                count_bottom = countsymbol_map[symbol][bottom]

                new_top = first_occurrence_map[symbol] + count_top
                new_bottom = first_occurrence_map[symbol] + count_bottom - 1
                #print(new_top, " ", new_bottom)
                top = new_top
                bottom = new_bottom
            else:
                top = 0
                bottom = -1
                break
        if len(current_pattern) == 0 and top <= bottom:
            match_count = bottom - top + 1
        else:
            match_count = 0

        result.append(match_count)

    return result
    pass


def first_occurance(first_col: List[str]) -> dict[str,int]:
    first_ocrs = {}
    for idx, symbol in enumerate(first_col):
        if symbol not in first_ocrs:
            first_ocrs[symbol] = idx
    return first_ocrs

def counted_symbols(last_col: List[str]): #return dict again?
    counted = {}
    symbols = last_col
    for symbol in symbols:
        counted[symbol] = [0] * len(last_col)
    symbol_counts = {}
    for symbol in symbols:
        symbol_counts[symbol] = 0

    for inx, symbol in enumerate(last_col):
        symbol_counts[symbol] += 1
        for sym in symbols:
            counted[sym][inx] = symbol_counts[sym]
    return counted
    pass

# Sample input:
# GGCGCCGC$TAGTCACACACGCCGTA
# ACC CCG CAG

# Sample output:
# 1 2 1
string = "GGCGCCGC$TAGTCACACACGCCGTA"
patterns = ["ACC", "CCG", "CAG"]
#print(better_bw_matching(string, patterns))

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