import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your greedy_motif_search_pseudocounts function here, along with any subroutines you need
def greedy_motif_search_pseudocounts(dna: list[str], k: int, t: int) -> list[str]:
    """Augments the GreedyMotifSearch algorithm with pseudocounts."""
    best_motifs = []
    for i in range(0, len(dna)):
        best_motifs.append(dna[i][0:k])
    for i in range(0, len(dna[0])-k+1):
        windows = [dna[0][i:i+k]]
        for j in range(1,t):
            prof = profile(windows) # replace this line for pseudocount file
            motif = profile_most_probable_kmer(dna[j], k, prof)
            windows.append(motif)
        if score(windows) < score(best_motifs):
            best_motifs = windows
    return best_motifs

def profile_most_probable_kmer(text: str, k: int,
                               profile: list[dict[str, float]]) -> str:
    """Identifies the most probable k-mer according to a given profile matrix.

    The profile matrix is represented as a list of columns, where the i-th element is a map
    whose keys are strings ("A", "C", "G", and "T") and whose values represent the probability
    associated with this symbol in the i-th column of the profile matrix.
    """

    # Text, profile, length of kmer
    # Loop through text with k size windows (sliding window)
    prob_dict = {}
    for i in range(len(text) - k + 1):
        window = text[i:i+k]
        prob = 1
        for j in range(len(window)):
            prob *= profile[j][window[j]]
        if window not in prob_dict:
            prob_dict[window] = prob
    #print(prob_dict)
        
    return max(prob_dict, key=prob_dict.get)

def profile(motif: list[str]): #NEEDS TO BE MODIFIED TO USE "Laplace's Rule of Succession to form Profile from motifs Motif1, …, Motifi-1"
    size = len(motif[0])
    length = len(motif)
    profile = []
    #count each nuc in each column
    for i in range(0, size):
        chars = {'A':1, 'C':1, 'G':1, 'T':1}
        for j in range(0, len(motif)):
            chars[motif[j][i]] += 1
        
        #divide that by the number of rows
        for key in chars:
            val = chars[key]/(length + 4)
            chars.update({key: val})
        profile.append(chars)
    return profile

def score (motifs: list[str]):
    s = 0
    prof = profile(motifs)
    consensus = ""
    for d in prof:
        consensus += max(d, key=d.get)
    for val in motifs:
        ham = hamming_distance(val, consensus)
        s += ham
    return s

def hamming_distance(p: str, q: str) -> int:
    """Calculate the Hamming distance between two strings."""
    #for each mismatche between two strings, add 1 to the hamming distance. a hamming distance of 0 is a perfect match.
    ham = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            #print(p[i])
            #print(q[i])
            ham += 1
    return ham

motif = ["TTTG", "ATGG", "ATTG", "ACGG"]
#print(profile(motif))

