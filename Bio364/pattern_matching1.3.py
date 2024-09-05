import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your pattern_matching function here, along with any subroutines you need
def pattern_matching(pattern: str, genome: str) -> list[int]:
    """Find all occurrences of a pattern in a genome."""
    indicies = []
    temp_index = ""
    pattern_len = len(pattern)
    for i in range(len(genome)):
        for j in range(len(pattern)):
            if genome[i] == pattern[j]:
                indicies.append(pattern[j])

    return indicies


pattern = "ATAT"
genome = "GATATATGCATATACTT"

print(pattern_matching(pattern, genome))