import math
import random
import copy

import heapq
from typing import List

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    """
    Implements a greedy TSP solver.

    Args:
        edges (list[list[float]]): Matrix of edge weights between cities.
        timer (Timer): Timer object to manage timeouts.

    Returns:
        list[SolutionStats]: A list of solutions with stats for each starting city.
    """
    stats = []  # List to store solutions
    n = len(edges)  # Number of cities
    cut_tree = CutTree(n)  # Track pruned portions of the tree

    # Loop through all starting cities
    for start_city in range(n):
        if timer.time_out():  # Stop if timer has expired
            break

        # Initialize tour and unvisited cities
        tour = [start_city]
        unvisited = set(range(n)) - {start_city}
        n_nodes_expanded = 1  # Nodes expanded (includes initial city)
        n_nodes_pruned = 0  # Pruned nodes

        while unvisited:
            current_city = tour[-1]
            best_edge = math.inf
            best_city = None

            # Find the nearest unvisited city
            for next_city in unvisited:
                if edges[current_city][next_city] < best_edge:
                    best_edge = edges[current_city][next_city]
                    best_city = next_city

            # If no valid edge is found, prune this path
            if best_city is None:
                n_nodes_pruned += 1
                break

            # Add the best city to the tour
            tour.append(best_city)
            unvisited.remove(best_city)
            n_nodes_expanded += 1

        # Complete the tour if all cities are visited
        if len(tour) == n:
            cost = score_tour(tour + [start_city], edges)  # Include return to start for scoring

            # Record the solution if it improves over previous ones
            if not stats or cost < stats[-1].score:
                stats.append(SolutionStats(
                    tour=tour,  # Exclude the return-to-start city from the tour
                    score=cost,
                    time=timer.time(),
                    max_queue_size=1,  # Greedy has no queue
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            else:
                # Prune the path if it doesn't improve the score
                n_nodes_pruned += 1
                cut_tree.cut(tour)

    # Return a no-solution result if no valid tour was found
    if not stats:
        return [SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=0,
            n_nodes_pruned=0,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        )]

    return stats

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    """
    Implements a Depth-First Search TSP solver.

    Args:
        edges (list[list[float]]): Matrix of edge weights between cities.
        timer (Timer): Timer object to manage timeouts.

    Returns:
        list[SolutionStats]: A list of solutions with stats for each starting city.
    """
    stats = []  # List to store solutions
    n = len(edges)  # Number of cities
    cut_tree = CutTree(n)  # Track pruned portions of the tree
    n_nodes_expanded = 0  # Counter for expanded nodes
    n_nodes_pruned = 0  # Counter for pruned nodes
    max_queue_size = 0  # Tracks the max size of the stack

    # Initialize the stack with the starting city
    stack = [[0]]  # Each element is a partial path (e.g., [0, 1, 2])
    
    while stack and not timer.time_out():
        current_path = stack.pop()  # Get the current partial path
        max_queue_size = max(max_queue_size, len(stack) + 1)
        n_nodes_expanded += 1

        # If we have a complete tour
        if len(current_path) == n + 1 and current_path[0] == current_path[-1]:
            cost = score_tour(current_path, edges)

            # Update the best solution found so far
            if not stats or cost < stats[-1].score:
                stats.append(SolutionStats(
                    tour=current_path[:-1],  # Exclude the return-to-start in SolutionStats
                    score=cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            continue

        # Expand current path to all unvisited cities
        current_city = current_path[-1]
        for next_city in range(n):
            # Only add valid next cities
            if (len(current_path) < n and next_city not in current_path) or \
               (len(current_path) == n and next_city == current_path[0]):  # Complete the tour
                # Avoid invalid edges
                if edges[current_city][next_city] != math.inf:
                    new_path = current_path + [next_city]
                    stack.append(new_path)  # Add the new path to the stack
                else:
                    n_nodes_pruned += 1
                    # Only prune paths with valid lengths
                    if len(current_path) < n:
                        cut_tree.cut(current_path + [next_city])  # Track pruning

    # If no valid tours are found, return a no-solution result
    if not stats:
        return [SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        )]

    return stats

def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    """
    Implements a Branch and Bound TSP solver using a reduced cost matrix for lower bounds.

    Args:
        edges (list[list[float]]): Matrix of edge weights between cities.
        timer (Timer): Timer object to manage timeouts.

    Returns:
        list[SolutionStats]: A list of solutions with stats for each solution found.
    """
    import math
    import copy

    n = len(edges)
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    max_queue_size = 0
    cut_tree = CutTree(n)

    # Initialize BSSF using the greedy tour
    initial_solutions = greedy_tour(edges, timer)
    if not initial_solutions or initial_solutions[0].score == math.inf:
        initial_BSSF = math.inf
        BSSF_tour = []
    else:
        initial_BSSF = initial_solutions[0].score
        BSSF_tour = initial_solutions[0].tour

    # Define the State class
    class State:
        def __init__(self, path, cost, reduced_matrix, lower_bound):
            self.path = path
            self.cost = cost
            self.reduced_matrix = reduced_matrix
            self.lower_bound = lower_bound

    # Function to reduce the matrix and calculate the reduction cost
    def reduce_matrix(matrix):
        n = len(matrix)
        reduced_matrix = [row[:] for row in matrix]
        reduction_cost = 0

        # Row reduction
        for i in range(n):
            row = reduced_matrix[i]
            min_value = min(row)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for j in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

        # Column reduction
        for j in range(n):
            col = [reduced_matrix[i][j] for i in range(n)]
            min_value = min(col)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for i in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

        return reduced_matrix, reduction_cost

    # Initial reduction
    initial_matrix, initial_reduction_cost = reduce_matrix(edges)
    initial_state = State(
        path=[0],
        cost=0,
        reduced_matrix=initial_matrix,
        lower_bound=initial_reduction_cost
    )

    # Initialize the stack with the initial state
    stack = [initial_state]

    while stack and not timer.time_out():
        current_state = stack.pop()
        n_nodes_expanded += 1
        max_queue_size = max(max_queue_size, len(stack) + 1)

        # Prune if lower bound is not promising
        if current_state.lower_bound >= initial_BSSF:
            n_nodes_pruned += 1
            continue

        current_path = current_state.path

        # Check if a complete tour is found
        if len(current_path) == n:
            last_city = current_path[-1]
            first_city = current_path[0]
            edge_back = current_state.reduced_matrix[last_city][first_city]
            if edge_back == math.inf:
                n_nodes_pruned += 1
                continue

            total_cost = current_state.cost + edge_back
            if total_cost < initial_BSSF:
                initial_BSSF = total_cost
                BSSF_tour = current_path + [first_city]
                stats.append(SolutionStats(
                    tour=current_path,
                    score=total_cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            else:
                n_nodes_pruned += 1
            continue

        current_city = current_path[-1]

        # Expand the current node
        for next_city in range(n):
            if next_city in current_path:
                continue  # Skip visited cities

            edge_cost = current_state.reduced_matrix[current_city][next_city]
            if edge_cost == math.inf:
                continue  # Skip non-existent edges

            # Create a deep copy of the reduced matrix
            child_matrix = [row[:] for row in current_state.reduced_matrix]

            # Update the cost
            cost = current_state.cost + edge_cost

            # Set the row of current city and column of next city to infinity
            for k in range(n):
                child_matrix[current_city][k] = math.inf
                child_matrix[k][next_city] = math.inf

            # Prevent returning to the previous city
            child_matrix[next_city][current_city] = math.inf

            # Reduce the new matrix
            child_matrix, reduction_cost = reduce_matrix(child_matrix)
            lower_bound = cost + reduction_cost

            # Prune if the new lower bound is not promising
            if lower_bound >= initial_BSSF:
                n_nodes_pruned += 1
                continue

            # Add the new state to the stack
            child_state = State(
                path=current_path + [next_city],
                cost=cost,
                reduced_matrix=child_matrix,
                lower_bound=lower_bound
            )
            stack.append(child_state)

    # If no solution was found, return a no-solution result
    if not stats:
        return [SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        )]

    return stats

def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    """
    Implements a Best-First Search (Smart Branch and Bound) TSP solver using a reduced cost matrix
    and a priority queue to prioritize deeper paths.

    Args:
        edges (list[list[float]]): Matrix of edge weights between cities.
        timer (Timer): Timer object to manage timeouts.

    Returns:
        list[SolutionStats]: A list of solutions with stats for each solution found.
    """
    import math
    import heapq
    import copy

    n = len(edges)
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    max_queue_size = 0
    cut_tree = CutTree(n)
    state_counter = 0  # To ensure unique entries in the priority queue

    # Initialize BSSF using the greedy tour
    initial_solutions = greedy_tour(edges, timer)
    if not initial_solutions or initial_solutions[0].score == math.inf:
        initial_BSSF = math.inf
        BSSF_tour = []
    else:
        # Find the best greedy solution (minimum score)
        initial_solutions_sorted = sorted(initial_solutions, key=lambda s: s.score)
        initial_BSSF = initial_solutions_sorted[0].score
        BSSF_tour = initial_solutions_sorted[0].tour
        stats.extend(initial_solutions_sorted)  # Include all greedy solutions in stats

    # Define the State class
    class State:
        def __init__(self, path, cost, reduced_matrix, lower_bound):
            self.path = path
            self.cost = cost
            self.reduced_matrix = reduced_matrix
            self.lower_bound = lower_bound

    # Function to reduce the matrix and calculate the reduction cost
    def reduce_matrix(matrix):
        n = len(matrix)
        reduced_matrix = [row[:] for row in matrix]
        reduction_cost = 0

        # Row reduction
        for i in range(n):
            row = reduced_matrix[i]
            min_value = min(row)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for j in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

        # Column reduction
        for j in range(n):
            col = [reduced_matrix[i][j] for i in range(n)]
            min_value = min(col)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for i in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

        return reduced_matrix, reduction_cost

    # Initialize the priority queue with all possible starting states
    priority_queue = []
    for start_city in range(n):
        if timer.time_out():
            break

        # Initial state for each starting city
        initial_matrix, initial_reduction_cost = reduce_matrix(edges)
        initial_state = State(
            path=[start_city],
            cost=0,
            reduced_matrix=initial_matrix,
            lower_bound=initial_reduction_cost
        )
        heapq.heappush(priority_queue, ((-len(initial_state.path), initial_state.lower_bound), state_counter, initial_state))
        state_counter += 1

    while priority_queue and not timer.time_out():
        (path_neg_len, current_lower_bound), _, current_state = heapq.heappop(priority_queue)
        n_nodes_expanded += 1
        max_queue_size = max(max_queue_size, len(priority_queue) + 1)

        # Prune if lower bound is not promising
        if current_state.lower_bound >= initial_BSSF:
            n_nodes_pruned += 1
            continue

        current_path = current_state.path

        # Check if a complete tour is found
        if len(current_path) == n:
            last_city = current_path[-1]
            first_city = current_path[0]
            edge_back = edges[last_city][first_city]  # Use original edges matrix here
            if edge_back == math.inf:
                n_nodes_pruned += 1
                continue

            total_cost = current_state.cost + edge_back
            if total_cost < initial_BSSF:
                initial_BSSF = total_cost
                BSSF_tour = current_path + [first_city]
                stats.append(SolutionStats(
                    tour=BSSF_tour,
                    score=total_cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            else:
                n_nodes_pruned += 1
            continue

        current_city = current_path[-1]

        # Expand the current node
        for next_city in range(n):
            if next_city in current_path:
                continue  # Skip visited cities

            edge_cost = current_state.reduced_matrix[current_city][next_city]
            if edge_cost == math.inf:
                continue  # Skip non-existent edges

            # Create a deep copy of the reduced matrix
            child_matrix = [row[:] for row in current_state.reduced_matrix]

            # Update the cost
            cost = current_state.cost + edge_cost

            # Set the row of current city and column of next city to infinity
            for k in range(n):
                child_matrix[current_city][k] = math.inf
                child_matrix[k][next_city] = math.inf

            # Prevent returning to the previous city
            child_matrix[next_city][current_city] = math.inf

            # Reduce the new matrix
            child_matrix, reduction_cost = reduce_matrix(child_matrix)
            lower_bound = cost + reduction_cost

            # Prune if the new lower bound is not promising
            if lower_bound >= initial_BSSF:
                n_nodes_pruned += 1
                continue

            # Add the new state to the priority queue
            child_state = State(
                path=current_path + [next_city],
                cost=cost,
                reduced_matrix=child_matrix,
                lower_bound=lower_bound
            )
            heapq.heappush(priority_queue, ((-len(child_state.path), child_state.lower_bound), state_counter, child_state))
            state_counter += 1

    # After the search, ensure that at least the initial BSSF is included
    if stats:
        # Sort the stats by score to have the best solutions first
        stats_sorted = sorted(stats, key=lambda s: s.score)
        return stats_sorted
    elif initial_solutions:
        # If no better solutions were found, return the greedy solutions
        return initial_solutions
    else:
        # Return a no-solution result
        return [SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        )]