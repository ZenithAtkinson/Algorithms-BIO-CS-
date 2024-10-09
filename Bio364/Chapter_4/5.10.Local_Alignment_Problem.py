import sys
import numpy as np
from typing import List, Dict, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your local_alignment function here, along with any subroutines you need
def local_alignment(match_reward: int, mismatch_penalty: int, indel_penalty: int, s: str, t: str) -> Tuple[int, str, str]:
    """
    Compute the local alignment of two strings based on match reward, mismatch penalty, and indel penalty.
    """
    #STEP BY STEP:
    # 1: Find highest count (local sink) either make a new double nested loop with a highest count or by tracking as we make the arrows
    # 2: Follow arrows from max count to top left, either by just checking arrow values or making a new backtrack(?)
    # 3: add character following backtrack until you reach a cell with a score of 0.

    back, score = LCSBackTrack(s, t, match_reward, mismatch_penalty, indel_penalty)
    max_val, max_row, max_col = FindHighestScore(score)
    #print(max_val)
    aligned_s, aligned_t = OutputLCS(backtrack=back, v=s, w=t, i=max_row, j=max_col, score=score)

    return max_val, aligned_s, aligned_t
    pass  # Implement the function logic here

def LCSBackTrack(v: str, w: str, match_reward: int, mismatch_penalty: int, indel_penalty: int):
    score = []
    Backtrack = []
    #i_val = 0
    #j_val = 0 - indel_penalty

    for i in range(len(v)+1):
        score.append([0] * (len(w)+1)) #everything 0
        Backtrack.append([0] * (len(w)+1))

    #print(scores)
    #backtrack init (like score, a matrix)

    for i in range (1, len(v)+1): #leave 0 col for base case 0's
        for j in range (1, len(w)+1):
            match = -mismatch_penalty
            if v[i-1] == w[j-1]: # str to int convert?
                match = match_reward
            #si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match } : up, left, diagonal : s is score
            #diag= score[i-1][j-1] + match

            score[i][j] = max(0, score[i-1][j] - indel_penalty, score[i][j-1] - indel_penalty, score[i-1][j-1] + match)
            if score[i][j] == 0:
                Backtrack[i][j] = "0"
            elif score[i][j] == score[i-1][j] - indel_penalty:
                Backtrack[i][j] = "v" #now up
            elif score[i][j] == score[i][j-1] - indel_penalty:
                Backtrack[i][j] = "->" #now left
            elif score[i][j] == score[i-1][j-1]+match:#si, j = si-1, j-1 + match
                Backtrack[i][j] = "↘"
            else:
                print("n/a err")
    #print(Backtrack)
    return(Backtrack, score)

def OutputLCS(backtrack, v, w, i, j, score) -> tuple[str, str]: #score for knowing when to ter
    #im gonna do iterative with while loop? 
    align_s = "" #1st str
    align_t = "" #2nd str

    if i == 0 or j == 0 or score[i][j] == 0:
        return "", ""
    elif backtrack[i][j] == "v" or j == 0:
        align_s, align_t = OutputLCS(backtrack, v, w, i - 1, j, score)
        return align_s + v[i-1], align_t + "-"
    elif backtrack[i][j] == "->" or i == 0:
        align_s, align_t = OutputLCS(backtrack, v, w, i, j - 1, score)
        return align_s + "-", align_t + w[j-1]
    elif backtrack[i][j] == "↘": #diagonal
        align_s, align_t = OutputLCS(backtrack, v, w, i - 1, j - 1, score)
        return align_s + v[i-1], align_t + w[j-1]
    else:
        print("shouldnt be here")


def FindHighestScore(score: list[list[int]]): 
    max_val = 0
    ret_Row = 0
    ret_Col = 0
    for row in range(len(score)):
        for col in range(len(score[row])):
            if max_val < score[row][col]:
                max_val = score[row][col]
                ret_Row = row
                ret_Col = col
    return max_val, ret_Row, ret_Col


match_reward = 1 #match
mismatch_penalty = 10 #mew
indel_penalty = 1 #sigma
s = "TTTTCCTT"
t = "CC"

print(local_alignment(match_reward, mismatch_penalty, indel_penalty, s, t))