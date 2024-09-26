 for i in range(len(kmers)):
        if k_prefixes not in kmer_dict:
            k_prefixes.append([])
        kmer_dict[k_prefixes[i]].append(k_suffixes[i])
    print(kmer_dict)
