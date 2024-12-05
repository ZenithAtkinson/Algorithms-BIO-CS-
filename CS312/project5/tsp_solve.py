import math
import random
import copy

import numpy as np #Could be better for heapq stuff

import heapq
from typing import List

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges)) #ToDo figure out wtf cut tree is

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1
        #print(tour)

        cost = score_tour(tour, edges)
        #print(cost)
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
    The basis of the greedy algorithm is that the cheapest available edge is the next edge taken.
    The greedy algorithm may run into dead-ends if the leading city (i.e. end of the current path) has no outbound edges (i.e. all outbound edges have cost of inf).
    Your greedy algorithm should search starting from city 0 first, then 1, 2, etc. Keep track of each solution found if it is better than the previous solution found. Run until all starting nodes have been considered or the timer runs out.
    """
    stats = []  #solutions
    n = len(edges)
    cut_tree = CutTree(n)

    for start_city in range(n):
        if timer.time_out(): #Do we need this, or does the test case handle it
            break

        tour = [start_city]
        unvisited = set(range(n)) - {start_city}
        n_nodes_expanded = 1  #(includes initial city)
        n_nodes_pruned = 0  #killed

        while unvisited:
            current_city = tour[-1]
            best_edge = math.inf
            best_city = None

            #Find the nearest unvisited city
            for next_city in unvisited:
                if edges[current_city][next_city] < best_edge:
                    best_edge = edges[current_city][next_city]
                    best_city = next_city
                    #print(best_city)

            #If no valid edge is found, kill path
            if best_city is None:
                n_nodes_pruned += 1
                break

            tour.append(best_city)
            unvisited.remove(best_city)
            n_nodes_expanded += 1

        if len(tour) == n:
            cost = score_tour(tour + [start_city], edges)
            #print(cost)

            #Record the solution if it improves over previous ones
            if not stats or cost < stats[-1].score:
                stats.append(SolutionStats(
                    tour=tour,
                    score=cost,
                    time=timer.time(),
                    max_queue_size=1,  #Greedy has no queue haha
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            else:
                # kill it
                n_nodes_pruned += 1
                cut_tree.cut(tour)

    #NO SOLUTION
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
    Put a path of [0] on the stack
    While the stack is not empty
    pop a path from the stack
    expand the path to all possible children paths
    if a child path is a solution that is better than the best solution so far, keep track of it
    else put the child path on the stack
    Return the list of solutions
    """
    stats = []
    n = len(edges) #Edge = City
    cut_tree = CutTree(n) #used to prune?
    n_nodes_expanded = 0
    n_nodes_pruned = 0 
    max_queue_size = 0 

    stack = [[0]]

    while stack and not timer.time_out():
        current_path = stack.pop()
        #print(current_path)
        max_queue_size = max(max_queue_size, len(stack) + 1)
        n_nodes_expanded += 1

        if len(current_path) == n + 1 and current_path[0] == current_path[-1]:
            cost = score_tour(current_path, edges)
            #Update the best solution found so far
            if not stats or cost < stats[-1].score:
                stats.append(SolutionStats(
                    tour=current_path[:-1],  #NO return-to-start in stats
                    score=cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            continue

        current_city = current_path[-1]
        for next_city in range(n):
            #print(next_city)
            #Check if next ones are valid
            if (len(current_path) < n and next_city not in current_path) or (len(current_path) == n and next_city == current_path[0]):
                if edges[current_city][next_city] != math.inf:
                    new_path = current_path + [next_city]
                    #print(new_path)
                    stack.append(new_path)  #
                else:
                    n_nodes_pruned += 1
                    #Check lengths
                    if len(current_path) < n:
                        cut_tree.cut(current_path + [next_city])

    #NO SOLUTION
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
    '''
    Your B&B implementation should compute a lower bound on each partial states (i.e. partial tour of the cities) using the reduced cost matrix as discussed in class.
    Then you should use the Best Solution So Far (BSSF) to prune partial states that have too-high of a lower bound (i.e. their lower bound score—the best that partial state could possibly do— is higher than the BSSF score, and therefor not worth searching further).
    Use a simple DFS expansion strategy (i.e. the same strategy used in your DFS implementation), but only put viable states on your queue. Partial states not put on the queue or not expanded are considered pruned.
    Your initial BSSF should be found using another simpler, quick algorithm. Your greedy algorithm is a very reasonable choice
    '''

    n = len(edges)
    #print(n)
    stats = []
    n_nodes_expanded = 0
    #print(n_nodes_expanded) 
    n_nodes_pruned = 0
    max_queue_size = 0
    cut_tree = CutTree(n) #Initialize cut tree for pruning

    initial_solutions = greedy_tour(edges, timer) #Find initial solutions using greedy algorithm (but dont bound it!!)
    #print(initial_solutions)
    if not initial_solutions or initial_solutions[0].score == math.inf:
        initial_BSSF = math.inf # Set BSSF to infinity if no initial solutions
        BSSF_tour = []
    else:
        #sort initial solutions by score
        initial_solutions_sorted = sorted(initial_solutions, key=lambda s: s.score)
        initial_BSSF = initial_solutions_sorted[0].score #best score so far
        BSSF_tour = initial_solutions_sorted[0].tour #best tour so far
        #print(initial_BSSF)
        stats.extend(initial_solutions_sorted) 

    class State:
        def __init__(self, path, cost, reduced_matrix, lower_bound):
            self.path = path
            self.cost = cost 
            self.reduced_matrix = reduced_matrix
            self.lower_bound = lower_bound  
    def reduce_matrix(matrix):
        n = len(matrix)
        reduced_matrix = [row[:] for row in matrix] #copy matrix
        reduction_cost = 0 #Total reduction cost

        for i in range(n):
            row = reduced_matrix[i]
            min_value = min(row)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for j in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

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

    stack = [] #For DFS

    for start_city in range(n):
        if timer.time_out():
            break
        #print(start_city) #current start city

        matrix, reduction_cost = reduce_matrix(edges) #reduce cost matrix
        #print(matrix)
        initial_state = State(
            path=[start_city],
            cost=0,
            reduced_matrix=matrix,
            lower_bound=reduction_cost
        )
        stack.append(initial_state)

    max_queue_size = max(max_queue_size, len(stack)) #update max queue size
    #print(max_queue_size)

    while stack and not timer.time_out():
        current_state = stack.pop()  #LIFO
        #print(current_state.path)
        n_nodes_expanded += 1 
        #print(n_nodes_expanded) 
        max_queue_size = max(max_queue_size, len(stack) + 1)
        #print(max_queue_size)

        if current_state.lower_bound >= initial_BSSF:
            n_nodes_pruned += 1 #kill it
            #print("State pruned due to lower bound")
            continue

        current_path = current_state.path
        #print(current_path)

        if len(current_path) == n:
            last_city = current_path[-1]
            first_city = current_path[0]
            edge_back = edges[last_city][first_city]
            if edge_back == math.inf:
                n_nodes_pruned += 1 #kill it
                #print("No return edge, state pruned")
                continue

            total_cost = current_state.cost + edge_back
            #print(total_cost)
            if total_cost < initial_BSSF:
                initial_BSSF = total_cost
                BSSF_tour = current_path + [first_city] #update best tour
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
                #print("New BSSF found! YAYA") #new best solution
            else:
                n_nodes_pruned += 1 #killk it
                #print("Tour cost higher than BSSF, pruned")
            continue

        current_city = current_path[-1]
        #print(current_city) 

        for next_city in range(n):
            if next_city in current_path:
                continue 
            #print(next_city)

            edge_cost = current_state.reduced_matrix[current_city][next_city]
            if edge_cost == math.inf:
                continue 
            #print(edge_cost)

            child_matrix = [row[:] for row in current_state.reduced_matrix] #Copy reduced matrix, too much memory?
            #print(child_matrix)

            cost = current_state.cost + edge_cost
            #print(cost)

            for k in range(n):
                child_matrix[current_city][k] = math.inf
                child_matrix[k][next_city] = math.inf

            child_matrix[next_city][current_city] = math.inf

            child_matrix, reduction_cost = reduce_matrix(child_matrix)
            lower_bound = cost + reduction_cost
            #print(lower_bound)

            if lower_bound >= initial_BSSF:
                n_nodes_pruned += 1 #Pruning
                #print("Child state pruned due to lower bound")
                continue

            child_state = State(
                path=current_path + [next_city],
                cost=cost,
                reduced_matrix=child_matrix,
                lower_bound=lower_bound
            )
            stack.append(child_state) #Add child state to stack

    if stats:
        #print("Sorting stats") #sorting solutions
        stats_sorted = sorted(stats, key=lambda s: s.score)
        stats_sorted.reverse()
        return stats_sorted
    elif initial_solutions:
        return initial_solutions
    else:
        #NO SOLUTION
        #print("No solution found") #no solutions available
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

def branch_and_bound_smart(edges: List[List[float]], timer) -> List['SolutionStats']:
    """
    Your smart B&B implementation should follow a similar pruning strategy to your B&B implementation; however, you should use a creative, intelligent expansion strategy to search the most promising regions of the search space first.
    One way to do this could be to change the logic of your state queue. Instead of using a simple last-in-first-out queue (i.e. a stack) like you do for DFS, consider some kind of priority queue that yields states that will help you find better solutions as quickly as possible.
    Do not use the lower bound as your priority key. If you are not sure why this advice is given, give it a try and see if you can tell why. :) The reasons will become more apparent with larger search spaces.
    For the best results, come up with a prioritization scheme that searches deep for solutions (i.e. prefers long partial paths—which are near to being solutions—over short ones) while still preferring states that are most likely to yield solutions with low scores.
    You might also consider searching in multiple phases: - first search for solutions (of any score) quickly that improve upon the BSSF - then search for the best possible solutions once you stop finding new (better) solutions so quickly
    There are various parts of your B&B algorithm that you can play with to make it search more intelligently. The purpose of this exercise is to explore the possibilities and come up with something useful. You may need to play with this a little. Be creative. Discuss strategies with your peers.
    **check discord
    """
    n = len(edges)
    #print(n)
    stats = [] 
    n_nodes_expanded = 0
    #print(n_nodes_expanded)
    n_nodes_pruned = 0
    max_queue_size = 0
    cut_tree = CutTree(n) #initialize cut tree for pruning

    # Initialize BSSF using the greedy tour
    initial_solutions = greedy_tour(edges, timer) #Find initial solutions using greedy algorithm (but dont bound it!!)
    #print(initial_solutions)
    if not initial_solutions or initial_solutions[0].score == math.inf:
        initial_BSSF = math.inf #set BSSF to infinity if  initial solutions
        BSSF_tour = []
    else:
        initial_solutions_sorted = sorted(initial_solutions, key=lambda s: s.score)
        initial_BSSF = initial_solutions_sorted[0].score
        BSSF_tour = initial_solutions_sorted[0].tour
        #INCLUDE initial solutions in stats
        stats.extend(initial_solutions_sorted)
    class State:
        def __init__(self, path, cost, reduced_matrix, lower_bound, depth):
            self.path = path  #current path as a list of city indices
            self.cost = cost  #current accumulated cost
            self.reduced_matrix = reduced_matrix  #current reduced cost matrix
            self.lower_bound = lower_bound  #current lower bound
            self.depth = depth  #depth in the search tree
            self.priority = None  #priority in the priority queue

        def compute_priority_phase1(self, alpha):
            #In Phase 1, prioritize deeper states and lower bounds
            #Using a tuple: (-depth, lower_bound)
            return (-self.depth, self.lower_bound)

        def compute_priority_phase2(self):
            #In Phase 2, prioritize states with lower bounds
            return (self.lower_bound,)

        #For heapq to compare states based on priority (this is our PQ)
        def __lt__(self, other):
            return self.priority < other.priority

    def reduce_matrix(matrix):
        n = len(matrix)
        reduced_matrix = [row[:] for row in matrix] #copy matrix
        reduction_cost = 0

        for i in range(n):
            row = reduced_matrix[i]
            min_value = min(row)
            if min_value == math.inf or min_value == 0:
                continue
            reduction_cost += min_value
            for j in range(n):
                if reduced_matrix[i][j] != math.inf:
                    reduced_matrix[i][j] -= min_value

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

    priority_queue = []
    phase = 1  #Start in Phase 1
    alpha = 1  #Play with this weight

    for start_city in range(n):
        if timer.time_out():
            break
        #print(start_city)

        matrix, reduction_cost = reduce_matrix(edges)
        #print(matrix) #reduced cost matrix
        initial_state = State(
            path=[start_city],
            cost=0,
            reduced_matrix=matrix,
            lower_bound=reduction_cost,
            depth=1  #starting depth is 1
        )
        #Getting phase 1 priority
        initial_state.priority = initial_state.compute_priority_phase1(alpha)
        # Push onto priority queue
        heapq.heappush(priority_queue, initial_state) #add initial state to priority queue
        #print("Initial state added to priority queue")

    max_queue_size = max(max_queue_size, len(priority_queue)) #update max queue size
    #print(max_queue_size

    while priority_queue and not timer.time_out():
        current_state = heapq.heappop(priority_queue) #remove state with highest priority
        n_nodes_expanded += 1 #increment expanded nodes
        #print(n_nodes_expanded)
        max_queue_size = max(max_queue_size, len(priority_queue) + 1)
        #print(max_queue_size)

        # Kill it if lower bound is not promising
        if current_state.lower_bound >= initial_BSSF:
            n_nodes_pruned += 1
            #print("State pruned due to high lower bound(?)")
            continue

        current_path = current_state.path
        #print(current_path)

        # Checkin for total tour
        if len(current_path) == n:
            last_city = current_path[-1]
            first_city = current_path[0]
            edge_back = edges[last_city][first_city]
            if edge_back == math.inf:
                n_nodes_pruned += 1 #kill it
                #print("No return edge found, pruning state")
                continue

            total_cost = current_state.cost + edge_back
            #print(total_cost)
            if total_cost < initial_BSSF:
                initial_BSSF = total_cost
                BSSF_tour = current_path.copy() #ensure tour length = n
                #print("New BSSF found") 

                stats.append(SolutionStats(
                    tour=current_path.copy(),  #ensure tour length = n
                    score=total_cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
                #print("solution recorded into stats")

                #Switchin to Phase 2 after finding the first complete solution
                if phase == 1:
                    phase = 2
                    #print("Switching to Phase 2")
                    # Recompute priorities
                    new_priority_queue = []
                    while priority_queue:
                        state = heapq.heappop(priority_queue)
                        state.priority = state.compute_priority_phase2()
                        heapq.heappush(new_priority_queue, state)
                        #print("Priority updated for state")
                    priority_queue = new_priority_queue
            else:
                n_nodes_pruned += 1 #kill it, too costly
                #print("Tour cost higher than BSSF, pruning state")
            continue

        current_city = current_path[-1]
        #print(current_city)

        for next_city in range(n):
            if next_city in current_path:
                continue  #skip visited cities
            #print(next_city)

            edge_cost = current_state.reduced_matrix[current_city][next_city]
            if edge_cost == math.inf:
                continue  #skip non-existent edges
            #print(edge_cost)

            # Create a deep copy of the reduced matrix, is this too memory intensive for Smart B&B?
            child_matrix = [row[:] for row in current_state.reduced_matrix]
            #print(child_matrix)

            cost = current_state.cost + edge_cost
            #print(cost) 
            for k in range(n):
                child_matrix[current_city][k] = math.inf
                child_matrix[k][next_city] = math.inf

            child_matrix[next_city][current_city] = math.inf
            child_matrix, reduction_cost = reduce_matrix(child_matrix)
            lower_bound = cost + reduction_cost
            #print(lower_bound)
            if lower_bound >= initial_BSSF:
                n_nodes_pruned += 1 #prune this child state
                #print("Child state pruned due to high lower bound")
                continue

            child_state = State(
                path=current_path + [next_city],
                cost=cost,
                reduced_matrix=child_matrix,
                lower_bound=lower_bound,
                depth=current_state.depth + 1
            )
            #print("Child state created")

            # New priority
            if phase == 1:
                # prioritize deeper states and lower bounds
                child_state.priority = child_state.compute_priority_phase1(alpha)
                #print("Priority computed for Phase 1") 
            else:
                # prioritize lower bounds
                child_state.priority = child_state.compute_priority_phase2()
                #print("Priority computed for Phase 2")

            #new state to the priority queue
            heapq.heappush(priority_queue, child_state)
            #print("Child state added to priority queue")

    if stats:
        #print("Sorting collected solutions")
        stats_sorted = sorted(stats, key=lambda s: s.score)
        stats_sorted.reverse()
        return stats_sorted
    elif initial_solutions:
        #print("Returning initial greedy solutions")
        return initial_solutions
    else:
        #print("No solution found")
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

