import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your profile_most_probable_kmer function here, along with any subroutines you need.

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
    print(prob_dict)
        
    return max(prob_dict, key=prob_dict.get)
            
    # calculate probability based on window
        # add to dictionary, where key = kmer, probability

def profile(motif: list[str]):
    size = len(motif[0])
    length = len(motif)
    profile = []
    #count each nuc in each column
    for i in range(0, size):
        chars = {'A':0, 'C':0, 'G':0, 'T':0}
        for j in range(0, len(motif)):
            chars[motif[j][i]] += 1
        profile.append(chars)
        #divide that by the number of rows
        for key in chars:
            val = round(chars[key]/length, 1)
            chars.update({key: val})
    return profile


profile_ = profile(["ATGCG","TGGCG","TGACG","TTCCG", "GTACA"])
print(profile_most_probable_kmer("ACCTGTTTATTGCCTAAGTTCCGGTACATTCCGAACAAACCCAATATAGCCCGAGGGCCT", 5, profile_))