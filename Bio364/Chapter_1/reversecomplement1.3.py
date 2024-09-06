import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your reverse_complement function here, along with any subroutines you need
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

sample_input = "AAAACCCGGT"

print(reverse_complement(sample_input))