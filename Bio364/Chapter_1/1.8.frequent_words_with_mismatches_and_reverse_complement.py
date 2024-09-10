import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your frequent_words_mismatches_reverse_complements function here, along with any subroutines you need
def frequent_words_mismatches_reverse_complements(text: str, k: int, d: int) -> list[str]:
    """Find the most frequent k-mers with up to d mismatches in a text, including reverse complements."""
    patterns = []
    freqMap = {}
    n = len(text)
    for i in range(n - k + 1):
        pattern = text[i:i+k]
        neighborhood = neighbors(pattern, d)
        for j in range (len(neighborhood)):
            neighbor = neighborhood[j]
            reverseNeighbor = reverse_complement(neighbor)
            if neighbor not in freqMap:
                freqMap[neighbor] = 1
            else:
                freqMap[neighbor] = freqMap[neighbor] + 1

            if reverseNeighbor not in freqMap:
                freqMap[reverseNeighbor] = 1
            else:
                freqMap[reverseNeighbor] = freqMap[reverseNeighbor] + 1
    m = max(freqMap.values())
    for pattern in freqMap.keys(): #is this keys?
        if freqMap[pattern] == m:
            patterns.append(pattern)
    return patterns

def reverse_complement(pattern: str) -> str:
    """Calculate the reverse complement of a DNA pattern."""
    #given a pattern... reverse it
    reversed_pattern = find_reverse(pattern)
    #and then complement it
    final_pattern = find_complement(reversed_pattern)
    return (final_pattern)

def find_complement(pattern: str) -> str:
    new_pattern = ""
    for char in pattern:
        if char == 'A':
            new_pattern = new_pattern + 'T'
        elif char == 'T':
            new_pattern = new_pattern + 'A'
        elif char == 'C':
            new_pattern = new_pattern + 'G'
        else:
            new_pattern = new_pattern + 'C'
    return new_pattern

def find_reverse(pattern: str) -> str:
    reversed_pattern = ""
    for char in reversed(pattern):
        reversed_pattern = reversed_pattern + char
    return reversed_pattern

def frequency_table(Text: str, k: int):
    freqDict = {}
    n = len(Text)
    for i in range(0, (n-k)+1):
        pattern = Text[i:i + k]
        if pattern in freqDict:
            freqDict[pattern] = freqDict[pattern]+1
        else:
            freqDict[pattern] = 1
    return freqDict

def neighbors(s: str, d: int) -> list[str]:
    """Generate neighbors of a string within a given Hamming distance."""
    if d == 0:
        return [s]
    if len(s) == 1:
        return ['A', 'C', 'G', 'T']
    neighborhood = []
    suffixNeighbors = neighbors(Suffix(s), d)
        #What is suffix? What does it mean?
        #I think that Suffix(pattern) is the pattern without its first value (so ACT would just be CT)
    #print(suffixNeighbors)
    for text in suffixNeighbors:
        if hamming_distance(Suffix(s), text) < d:
            for x in {"A", "C", "G", "T"}:
                neighborhood.append(x+text)
            #print(text)
        else:
            neighborhood.append(s[0]+text)
    return neighborhood

def Suffix(s: str):
    s_len = len(s)
    new_s = s[1:s_len]
    return new_s

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

text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
k = 4
d = 1

print(frequent_words_mismatches_reverse_complements(text, k, d))