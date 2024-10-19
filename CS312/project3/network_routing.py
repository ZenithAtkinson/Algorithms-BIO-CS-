import priority_queue_heap_array

def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    pq = priority_queue_heap_array.log_with_binary_heap()
    path = []

    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    pq.insert(source, dist[source])

    while len(pq.heap) > 0:
        current_node, current_dist = pq.delete_min()

        #print(f"Processing node {current_node} with distance {current_dist}")

        #break at target
        if current_node == target:
            break

        for neighbor, weight in graph[current_node].items():
            new_dist = current_dist + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node

                if neighbor in pq.pos_map:
                    pq.decrease_key(neighbor, new_dist)
                    #print(f"Decreased key of node {neighbor} to {new_dist}")
                else:
                    pq.insert(neighbor, new_dist)
                    #print(f"Inserted node {neighbor} with distance {new_dist} into the priority queue")

    #shortest path from source to target
    node = target
    while node is not None:
        path.insert(0, node)
        node = prev[node]

    return path, dist[target]


def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    pq = priority_queue_heap_array.linear_with_dictionary()
    path = []

    #init of everything
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    #ONLY SOURCE NODE
    pq.insert(source, dist[source])

    while len(pq.elements) > 0:
        current_node, current_dist = pq.delete_min()
        
        if current_node == target:
            break

        for neighbor, weight in graph[current_node].items():
            new_dist = current_dist + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node

                if neighbor in pq.elements:
                    pq.decrease_key(neighbor, new_dist)
                    #print(f"Decreased key of node {neighbor} to {new_dist}")
                else:
                    pq.insert(neighbor, new_dist)
 
                    #print(f"Inserted node {neighbor} with distance {new_dist} into the priority queue")

    node = target
    while node is not None:
        path.insert(0, node)
        node = prev[node]

    return path, dist[target]
