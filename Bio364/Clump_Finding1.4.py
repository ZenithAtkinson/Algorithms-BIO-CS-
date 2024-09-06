import sys

# Please do not remove package declarations because these are used by the autograder.

# Insert your find_clumps function here, along with any subroutines you need
def find_clumps(genome: str, k: int, l: int, t: int) -> list[str]:
    """Find patterns forming clumps in a genome."""
    patterns = []
    window = ""
    n = len(genome) #75
    for i in range(0, (n-k)+1):
        window = genome[i:i+ l]
        freqMap = frequency_table(window, k)
        for s in freqMap.keys():
            if freqMap[s] >= t:
                patterns.append(s)
                #print(s)
    
    patterns_final = (set(patterns))
    patterns_final = list(patterns_final)
    return patterns_final

def frequency_table(Text: str, k: int):
    freqDict = {}
    n = len(Text)
    for i in range(0, (n-k)+1):
        pattern = Text[i:i + k]
        if pattern in freqDict:
            freqDict[pattern] = freqDict[pattern]+1
        else:
            freqDict[pattern] = 1
    #print(freqDict)
    return freqDict

def read_in_file():
    #
    f = open("E_Coli.txt", "r")
    total_genome=f.read()
    return total_genome

genome="CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGGAAACATTGTAA"
k = 5
l = 50
t = 4

genome = read_in_file()
k = 9
l = 500
t = 3

final_list = (find_clumps(genome, k, l, t))
print(len(final_list))