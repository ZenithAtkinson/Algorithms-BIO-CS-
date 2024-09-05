import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your PatternCount function here, along with any subroutines you need
def pattern_count(text: str, pattern: str) -> int:
    count = 0
    for i in range(len(text) - len(pattern)+1):
        if text[i:i+len(pattern)] == pattern:
            count = count + 1
        print("count" + str(i))
    return count

text = "GCGCG"
pattern = "GCG"

result = pattern_count(text, pattern)
print(result)