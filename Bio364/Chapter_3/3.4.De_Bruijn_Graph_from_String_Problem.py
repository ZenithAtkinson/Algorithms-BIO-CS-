import sys
from typing import List, Dict, Iterable

# Please do not remove package declarations because these are used by the autograder.

# Insert your de_bruijn_string function here, along with any subroutines you need
def de_bruijn_string(text: str, k: int) -> Dict[str, List[str]]:
    """Forms the de Bruijn graph of a string."""
    #find all the kmers,
    kmers = []
    kmers = kmer_composition(text, k)
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

input_text = "ACGTGTATA"
k = 3
de_bruijn_string(input_text, k)