import math
import random

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
                    if len(current_path) <= n:  # Only prune paths of valid length
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
    return []


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
