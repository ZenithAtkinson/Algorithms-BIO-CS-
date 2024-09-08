def neighbors(s: str, d: int) -> list[str]:
    """Generate neighbors of a string within a given Hamming distance."""
    if d == 0:
        return(s)
    if len(s) == 1:
        return {'A', 'C', 'G', 'T'}
    neighborhood = []
    suffixNeighbors = neighbors(Suffix(s), d)
        #What is suffix? What does it mean?
        #I think that Suffix(pattern) is the pattern without its first value (so ACT would just be CT)
    print(suffixNeighbors)
    for text in suffixNeighbors:
        if hamming_distance(Suffix(s), text) < d:
            print(text)
    pass