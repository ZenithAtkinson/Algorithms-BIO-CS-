import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your frequent_words_with_mismatches function here, along with any subroutines you need
def frequent_words_with_mismatches(text: str, k: int, d: int) -> list[str]:
    """Find the most frequent k-mers with up to d mismatches in a text."""
    
    pass

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

text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
k = 4
d = 1

print(frequent_words_with_mismatches(text, pattern, d))