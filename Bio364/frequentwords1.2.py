import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your frequent_words function here, along with any subroutines you need
def frequent_words(text: str, k: int) -> list[str]:
    """Find the most frequent k-mers in a given text."""
    frequentPatterns = []
    freqDict = frequency_table(text, k)
    MAX = max(freqDict, key=freqDict.get)
    MAX = freqDict[MAX]
    for pattern in freqDict:
        print(freqDict[pattern])
        if freqDict[pattern] == MAX:
            frequentPatterns.append(pattern)
    return frequentPatterns

def frequency_table(Text: str, k: int):
    freqDict = {}
    n = len(Text)
    for i in range(0, (n-k)+1):
        pattern = Text[i:i + k]
        if pattern in freqDict:
            freqDict[pattern] = freqDict[pattern]+1
        else:
            freqDict[pattern] = 1
    #print(freqDict)
    return freqDict

text = "CAGTGGCAGATGACATTTTGCTGGTCGACTGGTTACAACAACGCCTGGGGCTTTTGAGCAACGAGACTTTTCAATGTTGCACCGTTTGCTGCATGATATTGAAAACAATATCACCAAATAAATAACGCCTTAGTAAGTAGCTTTT"
num = 4

print(frequent_words(text, num))