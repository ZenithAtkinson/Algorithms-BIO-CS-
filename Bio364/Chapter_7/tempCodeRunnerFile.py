from typing import List

def printer_i_hardly_know_her(matrix: List[List[str]]):
    beginS = '\t'
    header = matrix[0]
    print(beginS.join([''] + header))
    for row in matrix[1:]:
        print(beginS.join(row))
def print_HMM(states: List[str], trans_mans: List[List[float]], emissions: List[List[float]], alphabet: List[str]):
    """
    Prepares and prints the transition and emission matrices with headers,
    ensuring tab-separated values and probabilities rounded to three decimal places.

    Parameters:
    - states: List of state names.
    - trans_mans: 2D list of transition probabilities.
    - emissions: 2D list of emission probabilities.
    - alphabet: List of symbols in the alphabet.
    """
    def format_prob(prob: float) -> str:
        """
        Formats the probability to three decimal places.

        Parameters:
        - prob: The probability to format.

        Returns:
        - A string representation of the probability with three decimal places.
        """
        return f"{prob:.3f}"

    # Prepare Transition Matrix with Header
    transition_header = states
    transition_matrix = [transition_header]
    for i in range(len(states)):
        state = states[i]
        row_probs = trans_mans[i]
        # Format probabilities to three decimal places
        formatted_probs = [format_prob(prob) for prob in row_probs]
        # Create the row with state name followed by probabilities
        row = [state] + formatted_probs
        transition_matrix.append(row)

    # Prepare Emission Matrix with Header
    emission_header = alphabet
    emission_matrix = [emission_header]
    for i in range(len(states)):
        state = states[i]
        row_probs = emissions[i]
        if state.startswith('M') or state.startswith('I'):
            # Emitting states: format probabilities
            formatted_probs = [format_prob(prob) for prob in row_probs]
        else:
            # Non-emitting states: set probabilities to '0'
            formatted_probs = ['0'] * len(alphabet)
        # Create the row with state name followed by probabilities
        row = [state] + formatted_probs
        emission_matrix.append(row)

    # Print Transition Matrix
    printer_i_hardly_know_her(transition_matrix)

    # Print Separator
    print('--------')

    # Print Emission Matrix
    printer_i_hardly_know_her(emission_matrix)