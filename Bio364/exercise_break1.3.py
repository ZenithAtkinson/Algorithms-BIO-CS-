import sys

#Exercise Break: 
#Return a space-separated list of starting positions (in increasing order) where 
#CTTGATCAT appears as a substring in the Vibrio cholerae genome.

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

def read_in_file(file_path: str):
    #
    pass

##### MAIN CALL #####

#The pattern needs to read in the txt file for Vibrio_cholerae. Needs a separate funciton
pattern = "ATAT"
genome = "GATATATGCATATACTT"

print(pattern_matching(pattern, genome))