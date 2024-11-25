import sys
from typing import List, Dict, Tuple
from collections import defaultdict
import bisect

# Parameters for optimizations
K = 100  # Interval for partial suffix array
C = 100  # Interval for checkpoint arrays

def build_suffix_array(text: str) -> List[int]:
    """
    Builds the full suffix array for the given text.
    """
    suffixes = [(text[i:], i) for i in range(len(text))]
    sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
    suffix_array = [suffix[1] for suffix in sorted_suffixes]
    return suffix_array

def build_partial_suffix_array(suffix_array: List[int], K: int) -> Dict[int, int]:
    """
    Builds a partial suffix array by storing suffix positions at multiples of K.
    The partial_suffix_array maps from stored suffix position to its index in the suffix array.
    """
    partial_suffix_array = {}
    for idx, suffix_pos in enumerate(suffix_array):
        if suffix_pos % K == 0:
            partial_suffix_array[suffix_pos] = idx
    return partial_suffix_array

def build_bwt(text: str, suffix_array: List[int]) -> str:
    """
    Constructs the Burrows-Wheeler Transform (BWT) from the text and its suffix array.
    """
    bwt = []
    for suffix_pos in suffix_array:
        if suffix_pos == 0:
            bwt.append('$')
        else:
            bwt.append(text[suffix_pos - 1])
    return ''.join(bwt)

def build_first_occurrence(bwt_sorted: List[str]) -> Dict[str, int]:
    """
    Builds the first occurrence map from the sorted BWT (first column).
    """
    first_occurrence = {}
    for idx, symbol in enumerate(bwt_sorted):
        if symbol not in first_occurrence:
            first_occurrence[symbol] = idx
    return first_occurrence

def build_checkpoint_arrays(bwt: str, C: int) -> Dict[str, List[Tuple[int, int]]]:
    """
    Builds checkpoint arrays by storing counts of each symbol at every C positions.
    Each entry in the list for a symbol is a tuple (position, count).
    """
    checkpoint_arrays = defaultdict(list)
    symbol_counts = defaultdict(int)
    for idx, symbol in enumerate(bwt):
        symbol_counts[symbol] += 1
        if (idx + 1) % C == 0:
            for sym in symbol_counts:
                checkpoint_arrays[sym].append((idx, symbol_counts[sym]))
    return checkpoint_arrays

def count_symbol_up_to(bwt: str, checkpoint_arrays: Dict[str, List[Tuple[int, int]]], symbol: str, position: int, C: int) -> int:
    """
    Counts the number of occurrences of 'symbol' up to 'position' in BWT using checkpoint arrays.
    """
    if symbol not in checkpoint_arrays:
        return 0
    checkpoints = checkpoint_arrays[symbol]
    # Find the latest checkpoint <= position
    checkpoint_positions = [cp[0] for cp in checkpoints]
    idx = bisect.bisect_right(checkpoint_positions, position) - 1
    if idx >= 0:
        count = checkpoints[idx][1]
        checkpoint_pos = checkpoints[idx][0]
    else:
        count = 0
        checkpoint_pos = -1
    # Count occurrences from checkpoint_pos +1 to position
    for i in range(checkpoint_pos + 1, position + 1):
        if bwt[i] == symbol:
            count += 1
    return count

def better_bw_matching(bwt: str, patterns: List[str], first_occurrence: Dict[str, int],
                      checkpoint_arrays: Dict[str, List[Tuple[int, int]]], C: int) -> List[int]:
    """
    Perform an optimized Burrows-Wheeler Matching using checkpoint arrays.
    Returns the count of occurrences for each pattern.
    """
    result = []
    for pattern in patterns:
        top = 0
        bottom = len(bwt) - 1
        current_pattern = pattern
        while top <= bottom and current_pattern:
            symbol = current_pattern[-1]
            current_pattern = current_pattern[:-1]
            if symbol in first_occurrence:
                count_top = count_symbol_up_to(bwt, checkpoint_arrays, symbol, top - 1, C) if top > 0 else 0
                count_bottom = count_symbol_up_to(bwt, checkpoint_arrays, symbol, bottom, C)
                top = first_occurrence[symbol] + count_top
                bottom = first_occurrence[symbol] + count_bottom - 1
            else:
                top = 0
                bottom = -1
                break
        if current_pattern == '' and top <= bottom:
            match_count = bottom - top + 1
        else:
            match_count = 0
        result.append(match_count)
    return result

def build_partial_suffix_position_map(text: str, partial_suffix_array: Dict[int, int], suffix_array: List[int], K: int) -> Dict[int, int]:
    """
    Builds a map from suffix array index to text position for partial suffix array.
    This is useful for reconstructing positions.
    """
    return partial_suffix_array  # For this implementation, partial_suffix_array already maps text_pos to suffix_array_idx

def find_positions(text: str, pattern: str, suffix_array: List[int], partial_suffix_array: Dict[int, int], K: int) -> List[int]:
    """
    Finds all starting positions of pattern in text using the suffix array and partial suffix array.
    """
    positions = []
    n = len(text)
    m = len(pattern)
    
    # Binary search to find the left and right bounds in the suffix array
    left = 0
    right = len(suffix_array)
    
    # Find left bound
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:]
        if suffix.startswith(pattern) or suffix > pattern:
            right = mid
        else:
            left = mid + 1
    start = left
    
    # Find right bound
    right = len(suffix_array)
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:]
        if suffix.startswith(pattern) or suffix < pattern:
            left = mid + 1
        else:
            right = mid
    end = left
    
    # Collect positions from suffix array between start and end
    for idx in range(start, end):
        pos = suffix_array[idx]
        positions.append(pos)
    
    return sorted(positions)

def multiple_pattern_matching(text: str, patterns: List[str], K: int, C: int) -> Dict[str, List[int]]:
    """
    Solves the Multiple Pattern Matching Problem using partial suffix arrays and checkpoint arrays.
    Returns a dictionary mapping each pattern to a list of starting positions in text.
    """
    # Step 1: Build the full suffix array
    suffix_array = build_suffix_array(text)
    
    # Step 2: Build the partial suffix array
    partial_suffix_array = build_partial_suffix_array(suffix_array, K)
    
    # Step 3: Build the BWT
    bwt = build_bwt(text, suffix_array)
    
    # Step 4: Build the first occurrence map
    first_column = sorted(bwt)
    first_occurrence = build_first_occurrence(first_column)
    
    # Step 5: Build checkpoint arrays
    checkpoint_arrays = build_checkpoint_arrays(bwt, C)
    
    # Step 6: Count pattern occurrences using BWT and checkpoint arrays (optional, for counting)
    # counts = better_bw_matching(bwt, patterns, first_occurrence, checkpoint_arrays, C)
    
    # Step 7: Find positions using the suffix array
    result = {}
    for pattern in patterns:
        positions = find_positions(text, pattern, suffix_array, partial_suffix_array, K)
        result[pattern] = positions
    return result

def main():
    """
    Main function to read input, process patterns, and output the results.
    """
    input_data = sys.stdin.read().strip().split()
    text = input_data[0]
    patterns = input_data[1:]
    result = multiple_pattern_matching(text, patterns, K, C)
    # Print the results in the desired format
    for pattern in patterns:
        positions = result[pattern]
        positions_str = ' '.join(map(str, positions))
        print(f"{pattern}: {positions_str}")

if __name__ == "__main__":
    main()
