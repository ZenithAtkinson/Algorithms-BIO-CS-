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
    node = target
    
    #Init distance and previous nodes for Dijstras
    #for all u ∈ V do
        #dist(u) ← ∞
        #prev(u) ← NULL
    
    dist = {node: float('inf') for node in graph}
    #print(dist)
    prev = {node: None for node in graph} #No null?
    #print(prev)
    dist[source] = 0
    
    #+put them all into the queue
    for node in graph:
        pq.insert(node, dist[node])

    while len(pq.heap) > 0:
        current_node, current_dist = pq.delete_min()
        if current_node == target:
            break
        
        for neighbor, weight in graph[current_node].items():
            new_dist = current_dist + weight
            
            if new_dist < dist[neighbor]:
                #print(dist[neighbor])
                dist[neighbor] = new_dist
                prev[neighbor] = current_node
                pq.decrease_key(neighbor, new_dist)
                #print(dist[neighbor])

    while node is not None: #Null
        path.insert(0, node) 
        node = prev[node]
    #Includes cost (dist[target])
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
    #Same init idea as above (copy and paste)
    path = []
    node = target
    pq = priority_queue_heap_array.linear_with_dictionary()
    
    dist = {node: float('inf') for node in graph}
    #print(dist)
    prev = {node: None for node in graph} #No null?
    #print(prev)
    dist[source] = 0
    
    for node in graph:
        pq.insert(node, dist[node])
    #----------
        
    while len(pq.elements) > 0:
        current_node, current_dist = pq.delete_min()
        
        if current_node == target:
            break
        
        for neighbor, weight in graph[current_node].items():
            new_dist = current_dist + weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node
                pq.decrease_key(neighbor, new_dist)
    
    #Reconstucting path + cost
    while node is not None:
        #print(node)
        path.insert(0, node)
        node = prev[node]
    
    #Cost is dist[target] still
    return path, dist[target]


'''
Dijkstra(G, l, s)
for all u ∈ V do
    dist(u) ← ∞
    prev(u) ← NULL
dist(s) ← 0
H.makequeue(V) {distances as keys}
while H is not empty do
    u ← H.deletemin()
    for all edges (u, v) ∈ E do
        if dist(v) > dist(u) + l(u, v) then
            dist(v) ← dist(u) + l(u, v)
            prev(v) ← u
            H.decreasekey(v)
return dist, prev
'''