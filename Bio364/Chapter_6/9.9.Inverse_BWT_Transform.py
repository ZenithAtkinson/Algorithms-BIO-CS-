import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your inverse_burrows_wheeler_transform function here, along with any subroutines you need
def inverse_burrows_wheeler_transform(transform: str) -> str:
    """
    Generate the inverse of the Burrows-Wheeler Transform.
    """

    n = len(transform)
    #transform = Last column
    first_column = sorted(transform)

    #occurancs of LAST col
    last_Occurances = {}
    last_occurrence_indices = []
    for char in transform:
        #print(char)
        if char in last_Occurances:
            last_Occurances[char] += 1
        else:
            last_Occurances[char] = 1
        last_occurrence_indices.append(last_Occurances[char])

    #occurances of FIRST val
    first_Occurance = {}
    first_occurrence_indices = []
    for char in first_column:
        #print(char)
        if char in first_Occurance:
            first_Occurance[char] += 1
        else:
            first_Occurance[char] = 1
        first_occurrence_indices.append(first_Occurance[char])
    
    lastvsfirst = [0] * n
    first_column_dict = {}
    for index in range(n):
        char = first_column[index]
        OC = first_occurrence_indices[index]

        first_column_dict[(char, OC)] = index

    for i in range(n): #positions
        char = transform[i]
        OC = last_occurrence_indices[i]
        lastvsfirst[i] = first_column_dict[(char, OC)]
    #print(lastvsfirst)
    index = transform.index('$')
    #print(index)
    original_chars = []

    for i in range(n):
        index = lastvsfirst[index]
        #print(index)
        #print(first_column[index])
        original_chars.append(first_column[index]) 
    #print(original_chars)
    #reverse
    original_text = ''.join(reversed(original_chars))
    return original_text

    pass

input = "TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC"
print(inverse_burrows_wheeler_transform(input))