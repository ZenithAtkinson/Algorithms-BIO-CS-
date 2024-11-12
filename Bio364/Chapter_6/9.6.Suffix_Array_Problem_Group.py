import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your suffix_array function here, along with any subroutines you need
def suffix_array(text: str) -> List[int]:
    """
    Generate the suffix array for the given text.
    """
    suffix_dict = {}

    for index in range(len(text)):
        char = text[index]
        suffix = text[index:]

        suffix_dict[suffix] = index
    suffix_list = sorted(list(suffix_dict.keys()))
    final_list = []

    for char in suffix_list:
        final_list.append(suffix_dict[char])

    return final_list

    #Text
        #-> List of suffixes, and for each suffix, the starter index (dictionary)
    #Sort based on key
        #Based on sorted dictionary, print every value(index)

#input = "AACGATAGCGGTAGA$"
#print(suffix_array(input))