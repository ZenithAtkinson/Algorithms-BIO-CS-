import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your pattern_matching function here, along with any subroutines you need
def pattern_matching(pattern: str, genome: str) -> list[int]:
    """Find all occurrences of a pattern in a genome."""
    indicies = []
    temp_index = ""
    pattern_len = len(pattern)
    for i in range(len(genome)):
        sub_pattern = genome[i:i + len(pattern)]
            
        if sub_pattern == pattern:
            indicies.append(i)

    return indicies


#For each character in the pattern...
#Check the next PATTERN_LEN number of characters to see if they all match.
    #Loop through it 4 times for each character. Each character checks if i+n = the pattern.



pattern = "ATAT"
genome = "GATATATGCATATACTT"

print(pattern_matching(pattern, genome))