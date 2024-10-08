import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

sys.setrecursionlimit(10000) # Don't delete! This line is useful to ensure you have sufficient "recursion depth" to store the recursive calls needed for this problem.

# Insert your longest_common_subsequence function here, along with any subroutines you need
def longest_common_subsequence(s: str, t: str) -> str:
    #s = v, t = w
    """
    Calculate the longest common subsequence of two strings.
    """
    ret = ""
    the_backtrack = LCSBackTrack(s, t)
    #OutputLCS()
    longest_CS = OutputLCS(the_backtrack, s, len(s), len(t))
    #print(longest_CS)
    ret = longest_CS
    return ret
    # Implement the function logic here

def LCSBackTrack(v: str, w: str):
    score = []
    #Do i need to add all 0 values to the full score?
    for i in range(len(v)+1):
        row = []
        for j in range(len(w)+1):
            row.append(0)
        score.append(row)

    #backtrack init (like score, its a matrix)
    Backtrack = []
    for i in range(len(v)+1):
        row = []
        for j in range(len(w)+1):
            row.append(0)
        Backtrack.append(row)

    for i in range (len(v)+1):
        score[i][0] = 0
    for j in range (len(w)):
        score[0][j] = 0

    for i in range (1,len(v)):
        for j in range (1,len(w)):
            match = 0
            if v[i]-1 == w[j-1]: # str to int convert?
                match = 0
            #si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match }
            s[i][j] = max(s[i-1][j], s[i][j-1], s[i-1][j-1] + match)
            if s[i][j] == s[i-1][j]:
                Backtrack[i][j] = "v"
            elif s[i][j] == s[i][j-1]:
                Backtrack[i][j] = "->"
            elif s[i][j] == s[i-1][j-1+match]:#si, j = si-1, j-1 + match
                Backtrack[i][j] = "↘"
            else:
                print("n/a err")
    #print(Backtrack)
    return(Backtrack)

def OutputLCS(backtrack, v, i, j):
    if i == 0 or j == 0:
        return ""
    if backtrack[i][j] == "v":
        return OutputLCS(backtrack, v, i - 1, j)
    elif backtrack[i][j] == "->":
        return OutputLCS(backtrack, v, i, j - 1)
    else:
        return OutputLCS(backtrack, v, i - 1, j - 1) + v[i]

    pass

s = "GACT"
t = "ATG"

print(longest_common_subsequence(s, t))

# LCSBackTrack(v, w)
#     for i ← 0 to |v|
#         si, 0 ← 0
#     for j ← 0 to |w| 
#         s0, j ← 0
#     for i ← 1 to |v|
#         for j ← 1 to |w|
#             match ← 0
#             if vi-1 = wj-1
#                 match ← 1
#             si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match }
#             if si,j = si-1,j
#                 Backtracki, j ← "↓"
#             else if si, j = si, j-1
#                 Backtracki, j ← "→"
#             else if si, j = si-1, j-1 + match
#                 Backtracki, j ← "↘"
#     return Backtrack


# OutputLCS(backtrack, v, i, j)
#     if i = 0 or j = 0
#         return ""
#     if backtracki, j = "↓"
#         ﻿return OutputLCS(backtrack, v, i - 1, j)
#     else if backtracki, j = "→"
#         return OutputLCS(backtrack, v, i, j - 1)
#     else
#         return OutputLCS(backtrack, v, i - 1, j - 1) + vi