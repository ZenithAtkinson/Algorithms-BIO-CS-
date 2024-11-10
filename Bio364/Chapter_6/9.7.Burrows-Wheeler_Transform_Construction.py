import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your burrows_wheeler_transform function here, along with any subroutines you need
def burrows_wheeler_transform(text: str) -> str:
    """
    Generate the Burrows-Wheeler Transform of the given text.
    """

    #Get |text| number of strings
    #For each string, starting with OG text, move all characters one to the right
    all_Vals = []

    for i in range(len(text)):
        text = text[-1] + text[:-1]
        all_Vals.append(text)
    all_Vals = sorted(all_Vals)

    new_string = ""
    for string in all_Vals:
        new_string += string[-1]
    return new_string

input = "GCGTGCCTGGTCA$"
print(burrows_wheeler_transform(input))
