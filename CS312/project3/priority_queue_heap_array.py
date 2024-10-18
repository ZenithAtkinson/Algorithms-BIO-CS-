
class linear_with_dictionary:
    def __init__(vals):
        vals.elements = {} #dict

    def insert(vals, node, key):
        #Complexity: O(1)
        if node in vals.elements:
            if key < vals.elements[node]:
                vals.elements[node] = key
        else:
            vals.elements[node] = key
    
    def delete_min(vals):
        #Complexity: O(|V|)
        for node, key in vals.elements.items():
            smallest_node = node
            smallest_key = key
            break

        for node, key in vals.elements.items():
            if key < smallest_key:
                smallest_key = key
                smallest_node = node

        del vals.elements[smallest_node]
        
        return smallest_node, smallest_key
    
    def decrease_key(vals, node, NEW_key):
        #Complexity: O(1)
        if NEW_key < vals.elements[node]:
            vals.elements[node] = NEW_key
        else:
            print("Not smaller key (in decrease_key)")


class log_with_binary_heap:
    def __init__(vals):
        vals.heap = []
        vals.pos_map = {} #dict

    def insert(vals, node, key):
        vals.heap.append((node, key))

        ind = len(vals.heap) - 1
        vals.pos_map[node] = ind

        vals.heapifyUP(ind)
    
    def delete_min(vals):
        # Swap with last element, then heapify down
        vals.swap(0, len(vals.heap) - 1)

        smallest_node, smallest_key = vals.heap.pop() #Popping OG root from bfore
        del vals.pos_map[smallest_node]

        if len(vals.heap) > 0:
            vals.heapifyDOWN(0)
        
        return smallest_node, smallest_key
    
    def decrease_key(vals, node, NEW_key):
        index = vals.pos_map.get(node) #Grabbing EXACT node

        current = vals.heap[index][1]
        vals.heap[index] = (node, NEW_key) #Do I need to check if the new key is actually smaller?
        #print(vals.heap[node])
    
        vals.heapifyUP(index)

    def heapifyUP(vals, index):
        #Move node UP to correct pos
        parnt_index = (index - 1) // 2

        while index > 0 and vals.heap[index][1] < vals.heap[parnt_index][1]:
            vals.swap(index, parnt_index)
            index = parnt_index
            parnt_index = (index - 1) // 2
    
    def heapifyDOWN(vals, index):
        #Move node DOWN the heap (to correct pos)
        length = len(vals.heap)
        smallest = index

        left = 2 * index + 1
        right = 2 * index + 2

        #If left AND smaller:
        if left < length and vals.heap[left][1] < vals.heap[smallest][1]:
            smallest = left
        #If right AND smaller:
        if right < length and vals.heap[right][1] < vals.heap[smallest][1]:
            smallest = right

        #If smallest isnt current, swap them and move on with new one.
        if smallest != index:
            vals.swap(index, smallest) #implicit call of "vals" on swap
            vals.heapifyDOWN(smallest)
    def swap(vals, pos1, pos2):
        vals.heap[pos1], vals.heap[pos2] = vals.heap[pos2], vals.heap[pos1]
        
        vals.pos_map[vals.heap[pos1][0]] = pos1
        vals.pos_map[vals.heap[pos2][0]] = pos2


