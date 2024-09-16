import sys
import random

# Please do not remove package declarations because these are used by the autograder.

# Insert your gibbs_sampler function here, along with any subroutines you need
def gibbs_sampler(dna: list[str], k: int, t: int, n: int) -> list[str]:
    """Implements the GibbsSampling algorithm for motif finding."""
    #Random select k-mer from each dna string:
    kmers = []
    for pattern in dna:
        random_i = random.randint(0, len(pattern) - k)
        kmers.append(pattern[random_i : random_i + k])
    BestMotifs = kmers
    for j in range(1,n):
        i = random.randint(0, t-1) #getting random index (like before) for next pattern
        #exclude the motif i from profile below
        new_motifs = []
        for m in kmers:
            if m != kmers[i]:
                new_motifs.append(m)
        PROfile = profile(new_motifs)
        #Motifi ← Profile-randomly generated k-mer in the i-th sequence
        i_motif = PROfile[i]

    pass

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

t = 0
n = 0
k = 3  #test other leng
dna = ['AGCTAGC', 'TGCATGC', 'TTGGCCA']
motifs = []

gibbs_sampler(dna, k t, n)