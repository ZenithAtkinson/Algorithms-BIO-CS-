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
    BestMotifs = kmers #set randomly selected mers to "best motifs"
    #print(BestMotifs)
    for j in range(n):
        #Choose randomly 1 motif to replace
        i = random.randint(0, t-1)
        #exclude the motif i from profile below, build profile on remaining motif
        new_motifs = []
        for m in kmers:
            if m != kmers[i]:
                new_motifs.append(m)
        #print(new_motifs)
        PROfile = profile_w_pseudocounts(new_motifs)

        #Determine probability of each possible kmer to replace the removed kmer
        #Motifi ← Profile-randomly generated k-mer in the i-th sequence (weighted random selection)
        motif_i = profile_random_kmer(PROfile, dna[i], k) #Profile-randomly generated kmer (2.9.3)
        kmers[i] = motif_i
        #get the new scores, and compare them. If new score is better than bestmotifs, replace it
        motif_score = score(kmers)
        best_score = score(BestMotifs)
        if motif_score < best_score:
            BestMotifs = kmers
    return BestMotifs

def profile_random_kmer(profilei: list[str], texti: str, k: int):
    kmers = []
    k_probs = []

    for i in range(len(texti) - k + 1):
        kmer = texti[i:i+k] 
        kmers.append(kmer)
        #given profile probabilities, whats the prob of each kmer in removed sequence?
        prob = 1
        for j in range(len(kmer)):
            prob *= profilei[j][kmer[j]]
        k_probs.append(prob)
    #See 2.9.2 for how to get new ran values              #Laplace’s Rule of Succession
    #new random values where new_prob = prob / 1 * prob_total
    '''new_k_probs = []
    total_prob = sum(k_probs) #total prob, divide by new percentage to add up to 1
    for p in k_probs:
        new_p = p / total_prob
        new_k_probs.append(new_p)
        #print(new_k_probs)'''
    
    #How to select new random value? SEE TA
        # weighted random selection:
    #culmulative probs:
    c_probs = []
    c_sum = 0
    for prob in k_probs:
        c_sum += prob
        c_probs.append(c_sum)
    #find random kmer (python random.uniform(lowerval, upperval))
    r_val = random.uniform(0, c_sum)        
    for i in range(len(c_probs)):
        #print(r_val)
        #print(c_probs[i])
        if r_val <= c_probs[i]:
            #print(kmers[i])
            return kmers[i]


def profile_w_pseudocounts(motif: list[str]):
    size = len(motif[0])
    length = len(motif)
    profile = []
    #count each nuc in each column
    for i in range(0, size):
        chars = {'A':1, 'C':1, 'G':1, 'T':1}
        for j in range(0, len(motif)):
            chars[motif[j][i]] += 1
        profile.append(chars)
        #divide that by the number of rows
        for key in chars:
            val = chars[key]/(length + 4) #look into removing this 4, it works with and without it 
            chars.update({key: val})
        profile.append(chars)
    return profile

def score (motifs: list[str]):
    s = 0
    prof = profile_w_pseudocounts(motifs)
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

t = 5
n = 100
k = 8  #test other leng
dna = ['CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA', 'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG', 'TAGTACCGAGACCGAAAGAAGTATACAGGCGT', 'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC', 'AATCCACCAGCTCCACGTGCAATGTTGGCCTA']
motifs = []

#print(gibbs_sampler(dna, k, t, n))

best_omotifs = None
best_oscore = float('inf')

for start in range(20):
    print(f"\n--- Run {start + 1} ---")
    
    motifs = gibbs_sampler(dna, k, t, n)
    
    current_score = score(motifs)
    
    print("Motifs found:", motifs)
    print(f"Score: {current_score}\n")
    
    if current_score < best_oscore:
        best_omotifs = motifs
        best_oscore = current_score

print("\n--- Best motifs after 20 random starts ---")
print("Best motifs:", best_omotifs)
print(f"Best score: {best_oscore}")


'''
run 1: Best motifs: ['CTCGGGGG', 'CCAAGGTG', 'ACCGAAAG', 'GGTGCACG', 'CCACCAGC']
Score: 21

run 2: Best motifs: ['TTCAGTAA', 'AGTGCCAA', 'GAGACCGA', 'TAGATCAA', 'TGCAATGT']
Score: 20

run 3: Best motifs: ['CGGGGGTG', 'GAGGTATG', 'CGAGACCG', 'GGTGCACG', 'CCACGTGC']
Score: 22

run 4: Best motifs: ['GGGGGTGT', 'GAGGTATG', 'AGAAGTAT', 'TCGGTGAA', 'TGTTGGCC']
Score: 22

run 5: Best motifs: ['GGGGTGTT', 'GGGCGAGG', 'CGAGACCG', 'GCACGTCG', 'AATGTTGG']
Score: 21

run 6: Best motifs: ['TAAACGGC', 'ATGTGTAA', 'AAGAAGTA', 'TAGATCAA', 'ATCCACCA']
Score: 21

run 7: Best motifs: ['AGTAAACG', 'GAGGTATG', 'AAAGAAGT', 'AGTTTCAG', 'AATGTTGG']
Score: 21

run 8: Best motifs: ['CCTCTCGG', 'AGTGCCAA', 'ACCGAAAG', 'CACGTCGG', 'CCAGCTCC']
Score: 21

run 9: Best motifs: ['GTAAACGG', 'GGCGAGGT', 'TATACAGG', 'CACGTCGG', 'AATGTTGG']
Score: 22

run 10: Best motifs: ['TCAGTAAA', 'TGTAAGTG', 'CGAAAGAA', 'GGTGAACC', 'GTGCAATG']
Score: 21
'''