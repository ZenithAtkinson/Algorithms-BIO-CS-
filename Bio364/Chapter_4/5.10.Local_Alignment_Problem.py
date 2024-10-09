import sys
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
    # 3: Add character following backtrack until you reach a cell with a score of 0.


    pass  # Implement the function logic here

def LCSBackTrack(v: str, w: str, match_reward: int, mismatch_penalty: int, indel_penalty: int):
    score = []
    Backtrack = []
    i_val = 0
    j_val = 0 - indel_penalty

    for i in range(len(v)+1):
        score.append([i_val])
        Backtrack.append([0])
        i_val -= indel_penalty
        for j in range (1, len(w)+1):
            if i == 0:
                score[i].append(j_val)
                j_val -= indel_penalty
            else:
                score[i].append(0)
            Backtrack[i].append(0)

    #print(scores)
    #backtrack init (like score, a matrix)

    for i in range (1, len(v)+1): #leave 0 col for base case 0's
        for j in range (1, len(w)+1):
            match = -mismatch_penalty
            if v[i-1] == w[j-1]: # str to int convert?
                match = match_reward
            #si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match } : up, left, diagonal : s is score

            score[i][j] = max(score[i-1][j] - indel_penalty, score[i][j-1] - indel_penalty, score[i-1][j-1] + match)
            if score[i][j] == score[i-1][j] - indel_penalty:
                Backtrack[i][j] = "v"
            elif score[i][j] == score[i][j-1] - indel_penalty:
                Backtrack[i][j] = "->"
            elif score[i][j] == score[i-1][j-1]+match:#si, j = si-1, j-1 + match
                Backtrack[i][j] = "↘"
            else:
                print("n/a err")
    #print(Backtrack)
    return(Backtrack)

def OutputLCS(backtrack, v, w, i, j) -> tuple[str, str]:
    if i == 0 and j == 0:
        return "", ""
    elif backtrack[i][j] == "v" or j == 0:
        out = OutputLCS(backtrack, v, w, i - 1, j)
        return out[0] + v[i-1], out[1] + "-"
    elif backtrack[i][j] == "->" or i == 0:
        out = OutputLCS(backtrack, v, w, i, j - 1)
        return out[0] + "-", out[1] + w[j-1]
    else: #diagonal
        out = OutputLCS(backtrack, v, w, i - 1, j - 1)
        return out[0] + v[i-1], out[1] + w[j-1]
    

def FindHighestScore(score: list[int][int]):
    max_val = 0
    ret_Row = 0
    ret_Col = 0
    for row in score:
        for i in row:
            if max_val < i:
                max_val = i
                ret_Col = i
                ret_Row = row
    return max_val, ret_Row, ret_Col    


match_reward = 1 #match
mismatch_penalty = 10 #mew
indel_penalty = 1 #sigma
s = "TTTTCCTT"
t = "CC"

print(local_alignment(match_reward, mismatch_penalty, indel_penalty, s, t))