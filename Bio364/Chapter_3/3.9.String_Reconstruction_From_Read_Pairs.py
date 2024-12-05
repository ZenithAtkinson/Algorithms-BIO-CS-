import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Split the paired reads
# Make de Bruijn graph
# Find Eulerian paths
# Merge prefix + suffix

# Insert your StringReconstructionReadPairs function here, along with any subroutines you need
def StringReconstructionReadPairs(PairedReads: List[Tuple[str, str]], k: int, d: int) -> str:
    """
    Reconstructs a genome string from its paired (k, d)-mer composition.

    Parameters:
        PairedReads (List[Tuple[str, str]]): List of paired k-mers as tuples (Read1, Read2).
        k (int): Length of each k-mer.
        d (int): Gap distance between paired k-mers.

    Returns:
        str: The reconstructed genome string, or a message indicating failure.
    """
    return get_gapped(PairedReads, k, d)

def string_reconstruction(patterns: List[str], k: int) -> str:  #Needs a total rework (done?)
    de_brewin = de_bruijn_string(patterns, k)
    path = eulerian_path(de_brewin)

    final = ""
    first = True
    for i in path:
        if first:
            final += i
            first = False
        else:
            final += i[-1]
            #print(final)
    return final

def de_bruijn_string(kmers: List[str], k: int) -> Dict[str, List[str]]:
    """
    Constructs the de Bruijn graph from a list of k-mers.

    Parameters:
        kmers (List[str]): List of k-mers.
        k (int): Length of each k-mer.

    Returns:
        Dict[str, List[str]]: The de Bruijn graph represented as an adjacency list.
    """
    #Given a (k, d)-mer (a1 ... ak | b1 ... bk), we define its prefix as the (k − 1, d + 1)-mer (a1 ... ak-1 | b1 ... bk-1), 
    #and its suffix as the (k − 1, d + 1)-mer (a2 ... ak | b2 ... bk). For example, Prefix((GAC|TCA)) = (GA|TC) and Suffix((GAC|TCA)) = 
    #(AC|CA).
    #No more graph
    kmer_dict = {}
    k_prefixes = get_prefixes(kmers, k)
    k_suffixes = get_suffixes(kmers, k)

    for i in range(len(kmers)):
        if k_prefixes[i] not in kmer_dict:
            kmer_dict[k_prefixes[i]] = []
        kmer_dict[k_prefixes[i]].append(k_suffixes[i])

    return kmer_dict

def kmer_composition(text: str, k: int) -> Iterable[str]:  # 3.9.12, PairedCompositionGraph
    kmers = []
    for guy in range(len(text) - k + 1):
        kmer = text[guy:guy + k]
        kmers.append(kmer)
    return kmers

def get_prefixes(kmer_list: List[str], k: int) -> List[str]:  #Helpy
    prefixes = []
    for kmer in kmer_list:
        prefixes.append(kmer[:k - 1])
    #print(prefixes)
    return prefixes

def get_suffixes(kmer_list: List[str], k: int) -> List[str]:  #Helpy
    suffixes = []
    for kmer in kmer_list:
        suffixes.append(kmer[1:k])
    #print(suffixes)
    return suffixes

def eulerian_path(g: Dict[str, List[str]]) -> Iterable[str]:
    """
    Finds an Eulerian path in the given de Bruijn graph.

    Parameters:
        g (Dict[str, List[str]]): The de Bruijn graph represented as an adjacency list.

    Returns:
        Iterable[str]: The sequence of nodes in the Eulerian path.
    """
    #start_node = get_start_node(graph)
    #stack = [start_node]
    #path = []
    IN_degree = {}
    OUT_degree = {}
    for node in g:
        OUT_degree[node] = len(g[node])
        for neighbor in g[node]:
            IN_degree[neighbor] = IN_degree.get(neighbor, 0) + 1

    start = None
    end = None
    for node in set(list(IN_degree.keys()) + list(OUT_degree.keys())):
        #print(node)
        out_deg = OUT_degree.get(node, 0)
        in_deg = IN_degree.get(node, 0)
        #print(out_deg, ", ", in_deg)

        if out_deg - in_deg == 1:
            start = node
        elif in_deg - out_deg == 1:
            end = node

    if start is None:
        start = next(iter(g))  #Just the first one

    stacker = [start]
    path = []
    current_graph = {}
    for node, neighbors in g.items():
        #print("Copying: ", node, neighbors)
        current_graph[node] = neighbors.copy()
    #print(stacker)
    while stacker:
        current = stacker[-1]
        if current in current_graph and current_graph[current]:
            next_node = current_graph[current].pop(0)
            stacker.append(next_node)
        else:
            path.append(stacker.pop())
    path = path[::-1]  #Reverse it
    return path

def get_gapped(gapped_patterns: List[Tuple[str, str]], k: int, d: int) -> str:
    """
    Reconstructs a string from a sequence of paired (k, d)-mers.

    Parameters:
        gapped_patterns (List[Tuple[str, str]]): List of paired k-mers as tuples (Read1, Read2).
        k (int): Length of each k-mer.
        d (int): Gap distance between paired k-mers.

    Returns:
        str: The reconstructed genome string, or a message indicating failure.
    """
    first_patterns = []
    second_patterns = []
    for read in gapped_patterns:
        if len(read) != 2:
            return "ERROR ERROR"
        first_patterns.append(read[0])
        second_patterns.append(read[1])

    prefix_string = string_reconstruction(first_patterns, k)
    suffix_string = string_reconstruction(second_patterns, k)

    # overlap by (k + d) characters
    #
    # The last (k + d) characters of prefix_string should equal the 1st (k + d) characters of suffix_string

    overlap_length = k + d
    if len(prefix_string) < overlap_length or len(suffix_string) < overlap_length:
        return "Uh oh. this shouldnt be here"

    prefix_overlap = prefix_string[-overlap_length:]
    suffix_overlap = suffix_string[:overlap_length]

    reconstructed_text = prefix_string + suffix_string[overlap_length:]
    return reconstructed_text

# Issue input:
# 2 1
# GG|GA GT|AT TG|TA GA|AC AT|CT
# input_data = sample_input.strip().split()
k = 2  # k-mer length
d = 1  # gap distance
# k = 50
# d = 200
# paired_reads = "GG|GA GT|AT TG|TA GA|AC AT|CT".split()
paired_reads = [tuple(read.split('|')) for read in "GG|GA GT|AT TG|TA GA|AC AT|CT".split()]

result = StringReconstructionReadPairs(paired_reads, k, d)
print(result)  #Should be GGTGATACT
