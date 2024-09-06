import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your MinimumSkew function here, along with any subroutines you need
def minimum_skew(genome: str) -> list[int]:
    """Find positions in a genome where the skew diagram attains a minimum."""
    skew_vals = [0]

    #Needs a list of vals (0 -1 -2 -1 0 1 2 2 1)
    #Given list of vals, find the min (separate function?)

    #Before this, we need to create the list.
    #When char = C, decrease the NEXT val.
    #WHen char = G, increase the NEXT val.

    for i in range(len(genome)):
        if genome[i] == "C":
            skew_vals.append(skew_vals[i]-1)
        elif genome[i] == "G":
            skew_vals.append(skew_vals[i]+1)
        else:
            skew_vals.append(skew_vals[i])

    min_val = min(skew_vals)

    min_indicies = []
    #print(skew_vals)
    for i in range(len(skew_vals)):
        if skew_vals[i] == min_val:
            min_indicies.append(i)
            
    
    return min_indicies

genome = "TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT"

vals = (minimum_skew(genome))
#for i in vals:
#    print(i, " ", end = "")