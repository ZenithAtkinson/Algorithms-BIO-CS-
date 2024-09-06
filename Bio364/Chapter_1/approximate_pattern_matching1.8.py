import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your approximate_pattern_matching function here, along with any subroutines you need
def approximate_pattern_matching(pattern: str, text: str, d: int) -> list[int]:
    """Find all starting positions where Pattern appears as a substring of Text with at most d mismatches."""
    #Combination of hamming_distance and pattern_matching?

    #Search for HAMMING DISTANCE occurrences.
    indicies = []
    temp_index = ""
    pattern_len = len(pattern)
    for i in range(len(text)-len(pattern)+1):
        sub_pattern = text[i:i + len(pattern)]
        ham_distance = hamming_distance(sub_pattern, pattern)
        if ham_distance <= d:
            indicies.append(i)
    return indicies

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

pattern = "ATTCTGGA"
text = "CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT"
d = 3

print(approximate_pattern_matching(pattern, text, d))