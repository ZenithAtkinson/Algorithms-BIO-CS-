import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your approximate_pattern_count function here, along with any subroutines you need
def approximate_pattern_count(text: str, pattern: str, d: int) -> int:
    """Count the occurrences of a pattern in a text, allowing for up to d mismatches."""
    count = 0
    for i in range(len(text) - len(pattern)+1):
        new_pattern = text[i:i + len(pattern)]
        #print(new_pattern)
        if(hamming_distance(pattern, new_pattern) <= d):
            count += 1
    return count

def hamming_distance(p: str, q: str) -> int:
    """Calculate the Hamming distance between two strings."""
    #for each mismatche between two strings, add 1 to the hamming distance. a hamming distance of 0 is a perfect match.
    ham = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            #print(p[i])
            #print(q[i])
            ham += 1
    #print(ham)
    return ham

pattern = "GAGG"
text = "TTTAGAGCCTTCAGAGG"
d = 2

print(approximate_pattern_count(text, pattern, d))