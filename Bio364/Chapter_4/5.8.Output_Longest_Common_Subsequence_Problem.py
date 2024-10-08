import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

sys.setrecursionlimit(10000) # Don't delete! This line is useful to ensure you have sufficient "recursion depth" to store the recursive calls needed for this problem.

# Insert your longest_common_subsequence function here, along with any subroutines you need
def longest_common_subsequence(s: str, t: str) -> str:
    """
    Calculate the longest common subsequence of two strings.
    """
    ret = ""

    


    return ret
    # Implement the function logic here


# OutputLCS(backtrack, v, i, j)
#     if i = 0 or j = 0
#         return ""
#     if backtracki, j = "↓"
#         ﻿return OutputLCS(backtrack, v, i - 1, j)
#     else if backtracki, j = "→"
#         return OutputLCS(backtrack, v, i, j - 1)
#     else
#         return OutputLCS(backtrack, v, i - 1, j - 1) + vi

s = "GACT"
t = "ATG"

print(longest_common_subsequence(s, t))