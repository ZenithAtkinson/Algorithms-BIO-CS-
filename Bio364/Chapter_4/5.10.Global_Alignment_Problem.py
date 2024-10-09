import sys
from typing import List, Dict, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your global_alignment function here, along with any subroutines you need
def global_alignment(match_reward: int, mismatch_penalty: int, indel_penalty: int,
                     s: str, t: str) -> Tuple[int, str, str]:
    """
    Compute the global alignment of two strings based on given rewards and penalties.

    Args:
    match_reward (int): The reward for a match between two characters.
    mismatch_penalty (int): The penalty for a mismatch between two characters.
    indel_penalty (int): The penalty for an insertion or deletion.
    s (str): The first string.
    t (str): The second string.

    Returns:
    Tuple[int, str, str]: A tuple containing the alignment score and the aligned strings.
    """

    #Init the scoring matrix
    #Backtrack matrix needed?
    ret = LCSBackTrack(s, t, match_reward, mismatch_penalty, indel_penalty)
    ret1 = OutputLCS(ret, s, t, len(s), len(t))
    score = 0
    #print(ret1)
    for i in range(0, len(ret1[0])):
        if ret1[0][i] == ret1[1][i]:
            score += match_reward
        elif ret1[0][i] == "-" or ret1[1][i] == "-":
            score -= indel_penalty
        else:
            score -= mismatch_penalty

    return score, ret1[0], ret1[1]

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

match_reward = 1 #match
mismatch_penalty = 10 #mew
indel_penalty = 1 #sigma
s = "TTTTCCTT"
t = "CC"
print(global_alignment(match_reward, mismatch_penalty, indel_penalty, s, t))