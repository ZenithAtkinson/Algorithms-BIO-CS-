from priority_queues import ArrayPQ, HeapPQ


def test_pqs():
    items = list(range(10))
    array_pq = ArrayPQ(items)
    heap_pq = HeapPQ(items)

    array_pq.set_priority(7, 7)
    heap_pq.set_priority(7, 7)

    assert next(array_pq) == 7
    assert next(heap_pq) == 7

    array_pq.set_priority(3, 3)
    array_pq.set_priority(5, 1)
    heap_pq.set_priority(3, 3)
    heap_pq.set_priority(5, 1)

    assert next(array_pq) == 5
    assert next(array_pq) == 3

    assert next(heap_pq) == 5
    assert next(heap_pq) == 3
