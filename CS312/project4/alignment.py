import math
from typing import Tuple, List, Dict

def align( #default values?
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> Tuple[float, str | None, str | None]:

    if banded_width != -1:
        d = banded_width
        if abs(len(seq1) - len(seq2)) > d:
            return math.inf, None, None
    else:d = None

    def LCSBackTrack(v: str, w: str, d=None):
        m, n = len(v), len(w)

        score = []
        backtrack = []
        #Initializing EVERYTHING, score+backtrack
        if d is not None:
            for i in range(m + 1):
                score.append({})
                backtrack.append({})
        else:
            for i in range(m + 1):
                score_row = []
                backtrack_row = []
                for j in range(n + 1):
                    score_row.append(math.inf)
                    backtrack_row.append('')
                score.append(score_row)
                backtrack.append(backtrack_row)
        if d is None:
            score[0][0] = 0
        else:
            score[0][0] = 0

        if d is None:
            for i in range(1, m+1):
                score[i][0] = score[i-1][0] + indel_penalty
                backtrack[i][0] = 'v'
            for j in range(1, n+1):
                score[0][j] = score[0][j-1] + indel_penalty
                backtrack[0][j] = '->'
        else:
            for i in range(1, m+1):
                j = max(0, i - d)
                if abs(i - j) <= d:
                    score[i][j] = score[i-1].get(j, math.inf) + indel_penalty
                    backtrack[i][j] = 'v'
                    #print(score[i][j])
            for j in range(1, n+1):
                i = max(0, j - d)
                if abs(i - j) <= d:
                    score[i][j] = score[i].get(j-1, math.inf) + indel_penalty
                    backtrack[i][j] = '->'

        for i in range(1, m+1):
            j_start = 1 if d is None else max(1, i - d)
            j_end = n if d is None else min(n, i + d)
            
            for j in range(j_start, j_end+1):
                if d is not None and abs(i - j) > d:
                    continue
                    
                #Diagonal cost
                if v[i-1] == w[j-1]:
                    if d is None:
                        cost_diag = score[i-1][j-1] + match_award
                    else:
                        cost_diag = score[i-1].get(j-1, math.inf) + match_award
                else:
                    if d is None:
                        cost_diag = score[i-1][j-1] + sub_penalty
                    else:
                        cost_diag = score[i-1].get(j-1, math.inf) + sub_penalty
                
                #up and left costs
                if d is None:
                    cost_up = score[i-1][j] + indel_penalty
                    cost_left = score[i][j-1] + indel_penalty
                else:
                    cost_up = score[i-1].get(j, math.inf) + indel_penalty
                    cost_left = score[i].get(j-1, math.inf) + indel_penalty
                
                min_cost = min(cost_diag, cost_up, cost_left)
                if d is None:
                    score[i][j] = min_cost
                else:
                    score[i][j] = min_cost
                
                #Setting up backtrack
                if min_cost == cost_diag:
                    backtrack[i][j] = '↘'
                elif min_cost == cost_left:
                    backtrack[i][j] = '->'
                else:
                    backtrack[i][j] = 'v'

        if d is not None and len(seq2) not in score[len(seq1)]:
            return None, None
        return backtrack, score

    def OutputLCS(backtrack, v, w, d=None):
        if backtrack is None:
            return None, None
        aligned1 = []
        aligned2 = []
        i, j = len(v), len(w)
        while i > 0 or j > 0:
            if d is None:
                current = backtrack[i][j]
            else:
                current = backtrack[i].get(j, None)
                if current is None:
                    return None, None
                    
            if current == '↘':
                aligned1.append(v[i-1])
                aligned2.append(w[j-1])
                i -= 1
                j -= 1
            elif current == 'v':
                aligned1.append(v[i-1])
                aligned2.append('-')
                i -= 1
            elif current == '->':
                aligned1.append('-')
                aligned2.append(w[j-1])
                j -= 1
            else:
                return None, None
                
        aligned1.reverse()
        aligned2.reverse()
        return ''.join(aligned1), ''.join(aligned2)

    backtrack, score = LCSBackTrack(seq1, seq2, d)
    aligned1, aligned2 = OutputLCS(backtrack, seq1, seq2, d)
    #print(aligned1, aligned2)
    if aligned1 is None or aligned2 is None:
        return math.inf, None, None
    
    if d is None:
        total_cost = score[len(seq1)][len(seq2)]
    else:
        total_cost = score[len(seq1)].get(len(seq2), math.inf)
        
    return float(total_cost), aligned1, aligned2