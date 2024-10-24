import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

#Split the paired reads
#Make debruijn graph
#find eularian paths
#merge prefix + suffix

# Insert your StringReconstructionReadPairs function here, along with any subroutines you need
def StringReconstructionReadPairs(PairedReads: List[Tuple[str, str]],
                                  k: int, d: int) -> str:
    overlap = k + d #6

    #All prefix list
    paired_kmers = PairedReads

    pre_str, suf_str = string_reconstruction_paired(paired_kmers, k)

    overlap_length = len(pre_str) - overlap
    #overlap_length = len(read1_patterns)-overlap #-2? Can it even be neg?

    #print(overlap_length)
    #Given the prefix+suffix strings, we need to merge together
    prefix_overlap = pre_str[overlap:]
    suffix_overlap = suf_str[:overlap_length]
    #print(pre_str)
    #print(prefix_overlap)
    #print(suffix_overlap)
    if prefix_overlap != suffix_overlap:
        return "WRONG" + prefix_overlap

    fin_genome = pre_str + suf_str[overlap_length:]
    return fin_genome

    pass

# ALL MY OLD FUNCTIONS THAT ARE NEEDED:
def string_reconstruction(patterns: List[str], k: int) -> str:
    """Reconstructs a string from its k-mer composition."""
    dB = {}
    dB = de_bruijn_string(patterns, k)
    path = eulerian_path(dB)

    final = ""
    first = True
    #print(path)
    for i in path:
        if first:
            final+=i
            first = False
        else:
            final+= i[-1]
            #print(i[-1])
    
    #final = ""
    #for i in path:
    #    final+=(i[0])
    #
    #final_char = path[-1]
    #final+= (final_char[-1])

    return final

def string_reconstruction_paired(patterns: List[Tuple[str, str]], k: int):

    dB = paired_de_bruijn(patterns, k)
    path = eulerian_path(dB)
    #print(path)

    prefix_string = path[0][0]
    suffix_string = path[0][1]
    #suffix_string = path[1][0]
    #following path
    for node in path[1:]:
        #print(node)
        prefix_string += node[0][0]
        suffix_string += node[1][-1]

    return prefix_string, suffix_string


# Insert your de_bruijn_string function here, along with any subroutines you need
def de_bruijn_string(kmers: List[str], k: int):
    """Forms the de Bruijn graph of a string."""
    #find all the kmers,
    kmer_dict = {}

    #print(get_prefixes(kmers))
    #print(get_suffixes(kmers))
    k_prefixes = get_prefixes(kmers, k)
    k_suffixes = get_suffixes(kmers, k)
    # #and their prefixes/suffixes.
    #for each prefix, append it to a dictionary and add the suffixes as the key value

    for i in range(len(kmers)):
        if k_prefixes[i] not in kmer_dict:
            kmer_dict[ k_prefixes[i]] = []
        kmer_dict[k_prefixes[i]].append(k_suffixes[i])
    #print(kmer_dict)

    #for key, value in kmer_dict.items():
    #    print(f"{key}: {value}")

    #return dictionary list
    return kmer_dict

def paired_de_bruijn(kmers: List[Tuple[str, str]], k: int):
    #Given a (k, d)-mer (a1 ... ak | b1 ... bk), we define its prefix as the (k − 1, d + 1)-mer (a1 ... ak -1 | b1 ... bk - 1), and its suffix as the #(k - 1,d + 1)-mer (a2 ... ak | b2 ... bk). For example, Prefix((GAC|TCA)) = (GA|TC) and Suffix((GAC|TCA)) = (AC|CA).
    graph = {}

    for read1, read2 in kmers:
        prefix = (read1[:-1], read2[:-1]) 
        suffix = (read1[1:], read2[1:])
        if prefix not in graph:
            graph[prefix] = []
            #represents a path formed by |Text| - ( k + d + k) + 1
            #KEY: (k-1, d+1)-mer
            #VAL: (k-1, d+1)-mers.
        graph[prefix].append(suffix)

    return graph

def kmer_composition(text: str, k: int) -> Iterable[str]:
    """Forms the k-mer composition of a string."""
    #Given the text... find all kmers of given length k and return them as a list.
    kmers = []
    kmer = ""
    for c in range(len(text)-(k-1)):
        kmer = text[c:c+k]
        kmers.append(kmer)
    return kmers

def get_prefixes(kmer_list: list[str], k: int):
    prefixes = []
    for i in range(len(kmer_list)):
        kmer = kmer_list[i]
        prefixes.append(kmer[0:(k-1)]) #[0:2]
    #return a list of prefixes
    return prefixes

def get_suffixes(kmer_list: list[str], k: int):
    suffixes = []
    for i in range(len(kmer_list)): 
        kmer = kmer_list[i]
        suffixes.append(kmer[1:k]) #[1:3]
    #return a list of prefixes
    return suffixes

# Please do not remove package declarations because these are used by the autograder.

# Insert your eulerian_cycle function here, along with any subroutines you need
# g[u] is the list of neighbors of the vertex u
def eulerian_path(g: Dict[str, List[str]]) -> Iterable[str]:
    """Constructs an Eulerian pathe in a graph."""
    new_path = []
    start = get_start(g)
    end = get_end(g)
    if start != "NULL":
        if end in g.keys():
            g[end].append(start)
        else:
            g[end] = [start]


    key = list(g.keys())[0]
    #print(key)
    new_path.append(key)
    done = cycle_checker(g, new_path, key)
    while not done:
        i = 0
        #print("test")
        while i < (len(new_path)):
            if len(g[new_path[i]]) > 0:
                key = new_path[i]
                #print("key : ",key)
                break
            i += 1
        new_path2 = new_path[i:]
        new_path2.extend(new_path[1:i+1])
        new_path = new_path2
        done = cycle_checker(g, new_path, key)
    
    #print(g)
        
    if start != "NULL" or end != "NULL":
        for p in range(len(new_path)-1):
            if new_path[p] == end and new_path[p+1] == start:
                break        
        new_path2 = new_path[p:]
        new_path2.extend(new_path[1:p+1])
        new_path = new_path2
        new_path = new_path[1:]

    return new_path

def cycle_checker(g: Dict[str, List[str]], new_path: list, key: str):
    #Each time you move along the edge, take that given value out of the dictionary list.
        #Add it to a straight list which is the path.
    running = True
    while running:
        #Cut out each key, when it is empty
        #edge = key[0]
        edge = g[key].pop(0)
        key = edge
        new_path.append(edge)
        #print(g)
        #print(new_path)

        if (len(g[edge])==0):
            running == False
            break
    for i in g:
        if len(g[i]) >= 1:
            #print("its not finished")
            return False
        
    return True

def get_start(g: Dict[str, List[str]]):
    for i in g:
        count = 0
        for j in g:
            for k in g[j]:
                if k == i:
                    count+=1
        if (count < len(g[i])):
            return i
    return "NULL"

def get_end(g: Dict[str, List[str]]):
    for val in g.values():
        for item in val:
            if item not in g.keys():
                return item
    for i in g:
        count = 0
        for j in g:
            for k in g[j]:
                if k == i:
                    count+=1
        if (count > len(g[i])):
            return i
    return "NULL"


def compare_outputs(str1, str2):
    min_len = min(len(str1), len(str2))
    
    for i in range(min_len):
        if str1[i] != str2[i]:
            print(f"Mismatch at {i}: '{str1[i]}' != '{str2[i]}'")

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]
    #Split by '|'
    result = [tuple(line.strip().split('|')) for line in lines]
    
    return result

file_path = 'test_input_1.txt'
result = process_file(file_path)

#k = 4 #kmer length
#d = 2 #insert length
k = 50
d = 200

paired_reads = [('ACAC', 'CTCT'), ('ACAT', 'CTCA'), ('CACA', 'TCTC'), ('GACA', 'TCTC')]

#compare_outputs("ATCAATCTCGGGTTATCCTGGCAACGTTTTTGAGCATACCAAGTGGTCAGCGTTATTTAACGGCGTACCTATGTCGAGAAAATTTAACCACTTATATATCTTCCTGCATACACGCCAGCGTGCATTCCTAGCTTTGGTTTCTACGTGTAAAGGTTGTGCTCACTGTGAGTGTTGTTCCATATGGGCCGTTGGCACGCTAGGATGCTAACTCGCTCAATTCTCATCCTTTGCTTCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTCCCGCCTATGACGGGCTTAGCACACGCCTGGTATATCATAAAAAGACCGCAATCATTAGATCCCCGGACGAGTCGGGGGTGGTCTTCGGACAAGGTCAGAGTTTTCGCTCATTGGTCTGAAGTGTCCCTTTAGCCTAATCCAGTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTTTAGAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAAGTTGGTGTATACGTGGTGTATCGTCCCAGGTCCGTACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTGTCTAGATCAATCCCGACCCCAAAAGGCAATCCCCTCCGCTAACACTAGAAACAATGGTCGGCCTTGTCGGGCGCAATACATATCCCTAAGGTATTGACCAGTGCGCGGCGTTCTGCCGTTCCTATGGTAGATTAACGGTGTGCCCCGCATTGCCAAAGGCCAGAAGTTAGACCAAATTTGCGAGGCGCGTGCAGGGTCTAATGTGCGCTCAAATGATCAGATGTACTCCCCAAACGCACCCTTCGTGGGATGACCCCCGAGCTGCGCAGAATCAACGAAACTCCTGACTGAAAGGCTAAGTTCGGACGATGTCCCTTTCTAACATATACGGGCCTAGGCCCGCTCGTGAGTGGGTGACGCTTGACTTTAATAGTGTACCCGTAACGGGTTGGGCCTATACCCCGCGACTTGCAGTATCACACATTATCTGTGGAAGGGTTAGGGGCATCACTTGCGCGATAAGACGCTCTCCTTGGAGCAAGCCAAGCGGGGTACTATTTAACGATGATGCGATCTCCATCGAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACCAACTGCACGGCCTAGTCCTAGGCTTAGACAGGGTCATTACAGAAGCGCCTAGGTGCACGTTGCCCGTTGTGAACCTGATTCCGCAGCGTCAGTTCAGCACATTAGAGCAATACAAAAAACTTTCAGCCAGCGTTAGTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTTAAGGGCCTTGAAGAATGCCTCATCGTTATTGGCAGCCAAGGTCACGAGATTTGCGTGCAGGGCAATCCATGCGGGACATGTATGATCGCATGCTCAGGTAAAAAAATTGTGAGTCATACCTGGTTGAATTAGGATAAGGCAACCGAGACGATTGATGTTTATGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACCACTGGTAAACGAGGCCACTAATAATTGTAACAATTCTGGTAGTAATAAGTTTCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACGCTCTTCCCCCCAGTTACAGGAAGTCATCCCGACCCCTTCAGACGGAACGATCTGCCCCATTGGAAGTAGCTCTACACAGGCGTGACCGGAGTGCTAATACACGCGGGATCATAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTCCCCGTTATAGCAGAGAATTGGACAGAATTAAGAACTTTCACTTTCCATGTTCGTAGAGGCAACAAAATGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGGTGCGACGCGACCCTAGCGCGGTTATGGTATGGCTGGCGACAAAGTGCGTCAGTTGCCGGGGCAATAGGTCATCTGTGACTAGTTGGGCAGCCCGCGTTGATTAAGCCAGGCCGTATTCTCCATCAAGTGAAGCAGGTCCCCATCCATCAAGGCTAGGCGATTGGCTTCCTCTGCTCGCTGGGTACTGTTATGGAGGTAGTTAATGTGTTATTCTACCGAGGTGAGCGTGTGAACTGCATGAAAATCTGTACGACGGCATCCTAAGGCGGGAGGGACTTCTCTTATATCTCAAGGTTTCTACGGTTGTTATGTACGGCCCGTCGAACGCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACAACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATAAAAGCATGGGTTTAAAAGTTGCGTACTGACCCTTCGGTATGCTGGTTCAAGAAAGATAGGATAAGCTCGTAATTTAAAGTGGCGCTCTAAGGCGTGCCAGCAAAGGGAAATCGGCTAATGTAGCGAACGGTACGAGCGGACCCTCCTGTACTCCAATCCCCCCGGAGCGACGTGCTACCCATGTATGGAACACCAGAGCGCCGGAATCCAGCGATCCTAGTTCTTCCAGTGTCAAACTCCAAGCGGCACTCTCCGTGCCCCACAGGCCGTGCATCAAGTCGGCCAGATTAAACCTGCTAGCATGGCGGGTCAGTCCGATTCATGGCGACCCTTGACATGCGACGTAAACTGATAAATTTACACGTCTCCCGACTTCGTTGTATGTATGCGCACGATTCCCAGGTCAGACGTCCGCGCGAAGCGCCTACCGGTCTGTAAAGACACTTAAGCGGGAATATGGGATATGAATCAAGGCTAAGACTAAATCCGTCAACGTCAGGCAATCCCGTACGCAGGGCTCAAATGAACGGTGATGAACGAATAAGATCTCGCACCGAACGATCAGAGCAACTGTAGCTACTGGCCCCAAATTACGGGGGGGGCACGGCCATACGTGAGCTCTCGGTGGGATCGCACTCTCTCTATTCAGCTCTCTTGCGAGTACAGGATCTTATCGTGTCAAATACGGCCTCACCACGTGAAATGGCACAATGGACTTTGCGTCGGATGTCTCTATTTCAATCCCCTGATAGTGGGACACAATGGAGATTTTCTTAAGCGCTTATCAGAGTACACTCGAAGAAGGTTGCTGCTGGAAGATCTCCCTGGACCATACTAAGCTAGCGCCAACATCGCCAAGTCAGACCCGGGGGCTGTCCTCACGATAGAATGCGTCACGTGACGAGCGCAACTACGGTTAGTAATAGTTTTAGCAGAGTAGGCGGCAGTTTTCCCGGAATTTAGACAAAGCCTAAGGGCAAACGCGAGCGTCGGTCCACAAGACTGATGATTGACGGGGCTAAAAATTCACCAGGGAAAGGCCGGGCAGCTGTTGGTACTACGATTCATGCTACGCTACCATAGGCAGATACAATCTATTCGTTAGCTTTACCCTGGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGCATCCAGGGGTTCAGTCGTGTCTTACTCCGATCAGTCTCCTATGTCATTTATCGGTTGCTACGAGGTGATTCTGCAGAATAGCTAGGCCGAATGAATCGAGAGTTGTCTCGTGCAGACCAACGACACGTTTACAACACCATTCTCACTCTGTTCTTGCCGATTCAGATTCGGGTAGCTGAAGCACGGCGCGACTCACTTATTATGGTTTGAACCAATAAGGGTACGAGGAGCTGCAGAATAATAAGGTAGTCGGACAGACCTTTACAAACTGACACTAGAAAGAGTTACAAGAACGATGAGGATCGAGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTCAACTGTGAGAACGACATGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATCGTACGGCGAATAGTGGTTTCGCTGGCCCGGAAACGCTCCCAGTGCGAGCAGTCTCGGGAGCAAGATCCTCTACTACAGCCCTGGGTCGGGGTCCGTTATTCTTGGGACCCTTCTGACTGACTACGTTCGAGACCCCTTGTGCGGAAGTGAGCGCAGTGGTTTCTGCGTGCCGCCGAGGATTCGCTCTAAAGACCAACATTGCATGAAGCTATGTAGCCTCGGCCTCACTCCCCGCTTGTTGCTAATGGTCCGAACTGGCGCGCGTTTAGCACACCCACTGCCTGACTTGTATGATACGTTAAAAAGAAGGCTTGGAGAGTTACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTAGCCGTGTCTGGAGGTTGTGAAGCGTGGAGCATTTCGCTGTATCGAGTGTTGAATTTTCAACCCAACGTTTGCCGCACGTCTCCCAAGATATGGGATACTCAATGTTCGACGGGAACTCGGGGTATCGTCCAGCTCGCTCTTCCACCGATTAGGAAATCTCTGAAGCGCGCTGCCGTATTACCCGCTAGCTTATTCTGCGTGGGGCGTCGCAATTTAACGCTGCTAAGGCAGTCACAAGACACGATGCAAAAGCTTGAGAACAATGCTTGCGAGTTCGCGGTAAGTCGGTTGCTCCATGACATCTGGACCGCGGGTGTCCGTATTGTCGATTATAAACGCATCTTCGCCACCGCAGAACGTCATGGCGGTAGAGGTCTCGAGAATAGCGCGTCTGGTGAAAAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTGAGACCCGTTTTGGGGCCCAAGTGTCAACCGCGACAAGTGAGCTCCAGTACGAAGCGTAATGCCCTCTCCTCACCTTTTGTGAGCGTGAGTGTAGGAAGAACAAAGAGCTCATTGTACAAACTGTTAGACAGCTCACGGCAGGCGAGGGGTCCGTACAGGGATCCGATTCTGGAGCAAAAACCTTAGTTAGCCGCGTGACGGTCCGATCCCTCGTGCTTGTCCGAATGGCCTTCATGAAACGTACCATACGCCACCTGGAGTACATTTCGGGCTCAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAAATTCTATGGGTCAAAACGTTGATCTGAAGACATTTCATGCCTCAAATACAAATACCGTCCCTAAAGAGGTTGGGTATCCCTTACCGCGGTCCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGGCTTTCAGCCTTACGTGAGTAAACTTGTGCGAGGAAATTCCTTCGTCAATAGCAGACAGGCAAGTTGGCGGGGATTTCCTCAGTGTGATCCATGTAGCACAAGATGCATGTCTAGTGAAAAAGGTAGGATTCCAATTTAGGGGCTGGCGAGTCTTACATCCTTACCAGACGCAGATTCGCCTATCCCAGTGATGACCTCAAGCATTACTAGAAGGGGATTCCATAACATCACTCATTTGGAAGCTTTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTCGACGGGCCTTATGATAGGGTCAAGAACGGATCCGACGTAGCAGCTGCACTCTTTTATTGACCCGGTAAACGCAATTGTCCCGTCATGTAGTTTATAATTGTTTTTTTTCGGACACACCTCAAATATCACGTTAGGATTTCTATGACACTGATACTTGACCGAGCCAGACTACGCCGAACCAAGTCCGAAGAGAGCCATATTCTTCATTCCACATGCATTAGTACAACTCACCACTAACCACTTTTACTTTGACCTTCGCCATGGTGCCACAAGCCAGCTTGATCTTAGACGATTGGACCCTCTCTTGTAGCGTCACTCCGCCAAACTGCCTGTGGCCCCTGAGAGTCGTTTGGCTGCGCTAATATGTA", "ATCAATCTCGGGTTATCCTGGCAACGTTTTTGAGCATACCAAGTGGTCAGCGTTATTTAACGGCGTACCTATGTCGAGAAAATTTAACCACTTATATATCTTCCTGCATACACGCCAGCGTGCATTCCTAGCTTTGGTTTCTACGTGTAAAGGTTGTGCTCACTGTGAGTGTTGTTCCATATGGGCCGTTGGCACGCTAGGATGCTAACTCGCTCAATTCTCATCCTTTGCTTCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACGCTCTTCCCCCCAGTTACAGGAAGTCATCCCGACCCCTTCAGACGGAACGATCTGCCCCATTGGAAGTAGCTCTACACAGGCGTGACCGGAGTGCTAATACACGCGGGATCATAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGCATCCAGGGGTTCAGTCGTGTCTTACTCCGATCAGTCTCCTATGTCATTTATCGGTTGCTACGAGGTGATTCTGCAGAATAGCTAGGCCGAATGAATCGAGAGTTGTCTCGTGCAGACCAACGACACGTTTACAACACCATTCTCACTCTGTTCTTGCCGATTCAGATTCGGGTAGCTGAAGCACGGCGCGACTCACTTATTATGGTTTGAACCAATAAGGGTACGAGGAGCTGCAGAATAATAAGGTAGTCGGACAGACCTTTACAAACTGACACTAGAAAGAGTTACAAGAACGATGAGGATCGAGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGGTGCGACGCGACCCTAGCGCGGTTATGGTATGGCTGGCGACAAAGTGCGTCAGTTGCCGGGGCAATAGGTCATCTGTGACTAGTTGGGCAGCCCGCGTTGATTAAGCCAGGCCGTATTCTCCATCAAGTGAAGCAGGTCCCCATCCATCAAGGCTAGGCGATTGGCTTCCTCTGCTCGCTGGGTACTGTTATGGAGGTAGTTAATGTGTTATTCTACCGAGGTGAGCGTGTGAACTGCATGAAAATCTGTACGACGGCATCCTAAGGCGGGAGGGACTTCTCTTATATCTCAAGGTTTCTACGGTTGTTATGTACGGCCCGTCGAACGCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTCCCCGTTATAGCAGAGAATTGGACAGAATTAAGAACTTTCACTTTCCATGTTCGTAGAGGCAACAAAATGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGGCTTTCAGCCTTACGTGAGTAAACTTGTGCGAGGAAATTCCTTCGTCAATAGCAGACAGGCAAGTTGGCGGGGATTTCCTCAGTGTGATCCATGTAGCACAAGATGCATGTCTAGTGAAAAAGGTAGGATTCCAATTTAGGGGCTGGCGAGTCTTACATCCTTACCAGACGCAGATTCGCCTATCCCAGTGATGACCTCAAGCATTACTAGAAGGGGATTCCATAACATCACTCATTTGGAAGCTTTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTCAACTGTGAGAACGACATGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTGTCTAGATCAATCCCGACCCCAAAAGGCAATCCCCTCCGCTAACACTAGAAACAATGGTCGGCCTTGTCGGGCGCAATACATATCCCTAAGGTATTGACCAGTGCGCGGCGTTCTGCCGTTCCTATGGTAGATTAACGGTGTGCCCCGCATTGCCAAAGGCCAGAAGTTAGACCAAATTTGCGAGGCGCGTGCAGGGTCTAATGTGCGCTCAAATGATCAGATGTACTCCCCAAACGCACCCTTCGTGGGATGACCCCCGAGCTGCGCAGAATCAACGAAACTCCTGACTGAAAGGCTAAGTTCGGACGATGTCCCTTTCTAACATATACGGGCCTAGGCCCGCTCGTGAGTGGGTGACGCTTGACTTTAATAGTGTACCCGTAACGGGTTGGGCCTATACCCCGCGACTTGCAGTATCACACATTATCTGTGGAAGGGTTAGGGGCATCACTTGCGCGATAAGACGCTCTCCTTGGAGCAAGCCAAGCGGGGTACTATTTAACGATGATGCGATCTCCATCGAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACCAACTGCACGGCCTAGTCCTAGGCTTAGACAGGGTCATTACAGAAGCGCCTAGGTGCACGTTGCCCGTTGTGAACCTGATTCCGCAGCGTCAGTTCAGCACATTAGAGCAATACAAAAAACTTTCAGCCAGCGTTAGTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTCCCGCCTATGACGGGCTTAGCACACGCCTGGTATATCATAAAAAGACCGCAATCATTAGATCCCCGGACGAGTCGGGGGTGGTCTTCGGACAAGGTCAGAGTTTTCGCTCATTGGTCTGAAGTGTCCCTTTAGCCTAATCCAGTGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAAATTCTATGGGTCAAAACGTTGATCTGAAGACATTTCATGCCTCAAATACAAATACCGTCCCTAAAGAGGTTGGGTATCCCTTACCGCGGTCCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTTAAGGGCCTTGAAGAATGCCTCATCGTTATTGGCAGCCAAGGTCACGAGATTTGCGTGCAGGGCAATCCATGCGGGACATGTATGATCGCATGCTCAGGTAAAAAAATTGTGAGTCATACCTGGTTGAATTAGGATAAGGCAACCGAGACGATTGATGTTTATGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATCGTACGGCGAATAGTGGTTTCGCTGGCCCGGAAACGCTCCCAGTGCGAGCAGTCTCGGGAGCAAGATCCTCTACTACAGCCCTGGGTCGGGGTCCGTTATTCTTGGGACCCTTCTGACTGACTACGTTCGAGACCCCTTGTGCGGAAGTGAGCGCAGTGGTTTCTGCGTGCCGCCGAGGATTCGCTCTAAAGACCAACATTGCATGAAGCTATGTAGCCTCGGCCTCACTCCCCGCTTGTTGCTAATGGTCCGAACTGGCGCGCGTTTAGCACACCCACTGCCTGACTTGTATGATACGTTAAAAAGAAGGCTTGGAGAGTTACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATTAGCCGTGTCTGGAGGTTGTGAAGCGTGGAGCATTTCGCTGTATCGAGTGTTGAATTTTCAACCCAACGTTTGCCGCACGTCTCCCAAGATATGGGATACTCAATGTTCGACGGGAACTCGGGGTATCGTCCAGCTCGCTCTTCCACCGATTAGGAAATCTCTGAAGCGCGCTGCCGTATTACCCGCTAGCTTATTCTGCGTGGGGCGTCGCAATTTAACGCTGCTAAGGCAGTCACAAGACACGATGCAAAAGCTTGAGAACAATGCTTGCGAGTTCGCGGTAAGTCGGTTGCTCCATGACATCTGGACCGCGGGTGTCCGTATTGTCGATTATAAACGCATCTTCGCCACCGCAGAACGTCATGGCGGTAGAGGTCTCGAGAATAGCGCGTCTGGTGAAAAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAGTTTAGAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAACAACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAAAGTTGGTGTATACGTGGTGTATCGTCCCAGGTCCGTACGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAATAAAAGCATGGGTTTAAAAGTTGCGTACTGACCCTTCGGTATGCTGGTTCAAGAAAGATAGGATAAGCTCGTAATTTAAAGTGGCGCTCTAAGGCGTGCCAGCAAAGGGAAATCGGCTAATGTAGCGAACGGTACGAGCGGACCCTCCTGTACTCCAATCCCCCCGGAGCGACGTGCTACCCATGTATGGAACACCAGAGCGCCGGAATCCAGCGATCCTAGTTCTTCCAGTGTCAAACTCCAAGCGGCACTCTCCGTGCCCCACAGGCCGTGCATCAAGTCGGCCAGATTAAACCTGCTAGCATGGCGGGTCAGTCCGATTCATGGCGACCCTTGACATGCGACGTAAACTGATAAATTTACACGTCTCCCGACTTCGTTGTATGTATGCGCACGATTCCCAGGTCAGACGTCCGCGCGAAGCGCCTACCGGTCTGTAAAGACACTTAAGCGGGAATATGGGATATGAATCAAGGCTAAGACTAAATCCGTCAACGTCAGGCAATCCCGTACGCAGGGCTCAAATGAACGGTGATGAACGAATAAGATCTCGCACCGAACGATCAGAGCAACTGTAGCTACTGGCCCCAAATTACGGGGGGGGCACGGCCATACGTGAGCTCTCGGTGGGATCGCACTCTCTCTATTCAGCTCTCTTGCGAGTACAGGATCTTATCGTGTCAAATACGGCCTCACCACGTGAAATGGCACAATGGACTTTGCGTCGGATGTCTCTATTTCAATCCCCTGATAGTGGGACACAATGGAGATTTTCTTAAGCGCTTATCAGAGTACACTCGAAGAAGGTTGCTGCTGGAAGATCTCCCTGGACCATACTAAGCTAGCGCCAACATCGCCAAGTCAGACCCGGGGGCTGTCCTCACGATAGAATGCGTCACGTGACGAGCGCAACTACGGTTAGTAATAGTTTTAGCAGAGTAGGCGGCAGTTTTCCCGGAATTTAGACAAAGCCTAAGGGCAAACGCGAGCGTCGGTCCACAAGACTGATGATTGACGGGGCTAAAAATTCACCAGGGAAAGGCCGGGCAGCTGTTGGTACTACGATTCATGCTACGCTACCATAGGCAGATACAATCTATTCGTTAGCTTTACCCTGGGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTGAGACCCGTTTTGGGGCCCAAGTGTCAACCGCGACAAGTGAGCTCCAGTACGAAGCGTAATGCCCTCTCCTCACCTTTTGTGAGCGTGAGTGTAGGAAGAACAAAGAGCTCATTGTACAAACTGTTAGACAGCTCACGGCAGGCGAGGGGTCCGTACAGGGATCCGATTCTGGAGCAAAAACCTTAGTTAGCCGCGTGACGGTCCGATCCCTCGTGCTTGTCCGAATGGCCTTCATGAAACGTACCATACGCCACCTGGAGTACATTTCGGGCTCAGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACCACTGGTAAACGAGGCCACTAATAATTGTAACAATTCTGGTAGTAATAAGTTTCGTTACGCGGCCCACTATGCTGGAGCGGCATAGGGGTGCAATGTTACGCAACTCGACGGGCCTTATGATAGGGTCAAGAACGGATCCGACGTAGCAGCTGCACTCTTTTATTGACCCGGTAAACGCAATTGTCCCGTCATGTAGTTTATAATTGTTTTTTTTCGGACACACCTCAAATATCACGTTAGGATTTCTATGACACTGATACTTGACCGAGCCAGACTACGCCGAACCAAGTCCGAAGAGAGCCATATTCTTCATTCCACATGCATTAGTACAACTCACCACTAACCACTTTTACTTTGACCTTCGCCATGGTGCCACAAGCCAGCTTGATCTTAGACGATTGGACCCTCTCTTGTAGCGTCACTCCGCCAAACTGCCTGTGGCCCCTGAGAGTCGTTTGGCTGCGCTAATATGTA")

print(StringReconstructionReadPairs(result, k, d))
#print("GACACATCTCTCA")
#Correct output: GACACATCTCTCA
