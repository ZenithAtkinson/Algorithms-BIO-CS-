import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your bw_matching function here, along with any subroutines you need
def bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    first_column = sorted(bwt)
    last_column = list(bwt)

    LastToFirst = generate_first_to_last(bwt)
    result = []

    for pattern in patterns:
        top = 0
        bottom = len(bwt) - 1
        current_pattern = pattern
        found = True

        while top <= bottom:
            if len(current_pattern) > 0:
                #print(current_pattern)
                symbol = current_pattern[-1]
                current_pattern = current_pattern[:-1]

                first_occurrence = -1
                last_occurrence = -1
                #print(symbol)

                for i in range(top, bottom + 1):
                    if last_column[i] == symbol:
                        if first_occurrence == -1:
                            first_occurrence = i
                        last_occurrence = i

                if first_occurrence != -1:
                    top = LastToFirst[first_occurrence]
                    bottom = LastToFirst[last_occurrence]
                    #print(top)
                    #print(bottom)
                else:
                    found = False
                    break
            else:
                break

        if found and len(current_pattern) == 0:
            match_count = bottom - top + 1
        else: #no pattern
            match_count = 0
        result.append(match_count)

    return result
    pass

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
    print(all_Vals)
    all_Vals = sorted(all_Vals)

    new_string = ""
    for string in all_Vals:
        new_string += string[-1]
    return new_string

def generate_first_to_last(transform: str) -> List[int]: #Borrowed from inverse function
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

    first_column_dict = {}
    for index in range(n):
        char = first_column[index]
        occ = first_occurrence_indices[index]
        first_column_dict[(char, occ)] = index

    first_to_last = [0] * n
    for i in range(n):
        char = transform[i]
        occ = last_occurrence_indices[i]
        first_to_last[i] = first_column_dict[(char, occ)]
    #--- End of inverse function
    return first_to_last

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
patterns = ["CCT", "CAC", "GAG", "CAG", "ATC"]
#print(generate_first_to_last("smnpbnnaaaaa$a"))
print(bw_matching(input, patterns))
#print(inverse_burrows_wheeler_transform(input))
