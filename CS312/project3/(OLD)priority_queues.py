from math import inf as INF


class ArrayPQ:
    """Implements a PQ using an array."""

    def __init__(self, items):
        """Make the queue from items"""
        self.queue = {item: INF for item in items}

    def __bool__(self):
        """Return True if not empty"""
        return bool(self.queue)

    def __next__(self):
        """Return the min item and remove it from the queue"""
        item = min(self.queue, key=self.queue.get)
        del self.queue[item]
        return item

    def set_priority(self, item, priority):
        """Set the priority of node"""
        self.queue[item] = priority


class HeapPQ:
    """Use a heap to implement PQ"""

    def __init__(self, items):
        """Make the queue from items"""
        self.heap = [(INF, item) for item in items]
        self.lookup = {item: index for index, item in enumerate(items)}
        for index in reversed(range(len(self.heap))):
            self._percolate_up(index)

    def _swap(self, a, b):
        item_a = self.heap[a][1]
        item_b = self.heap[b][1]
        self.lookup[item_a] = b
        self.lookup[item_b] = a
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def _percolate_up(self, index):
        parent = index // 2
        if parent < index and self.heap[parent][0] > self.heap[index][0]:
            # Light element lower in the tree => move up
            self._swap(parent, index)
            self._percolate_up(parent)

    def _percolate_down(self, index):
        left = index * 2
        right = left + 1
        # If a child is lighter than index, swap index with the lighter child
        if (left < len(self.heap) and self.heap[index][0] > self.heap[left][0]) \
                or (right < len(self.heap) and self.heap[index][0] > self.heap[right][0]):
            lighter = left
            if right < len(self.heap) and self.heap[left][0] > self.heap[right][0]:
                # right is lighter that left, so use it
                lighter = right
            self._swap(index, lighter)
            self._percolate_down(lighter)

    def __str__(self):
        return str(self.heap)

    def __bool__(self):
        """Return True if not empty"""
        return bool(self.heap)

    def __next__(self):
        """Return the min item and remove it from the queue"""
        item = self.heap[0][1]
        self._swap(0, -1)
        del self.lookup[item]
        del self.heap[-1]
        self._percolate_down(0)
        return item

    def set_priority(self, item, priority):
        """Set the priority of node"""
        index = self.lookup[item]
        old_priority = self.heap[index][0]
        self.heap[index] = (priority, item)
        if old_priority > priority:
            # Item got lighter, move up
            self._percolate_up(index)
        else:
            self._percolate_down(index)
