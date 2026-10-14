import heapq


def shortest(graph, start, goal):
    if any(cost < 0 for edges in graph.values()
           for _, cost in edges):
        raise ValueError("отрицательная стоимость")
    queue = [(0, start, (start,))]
    best = {start: 0}
    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost != best[node]:
            continue
        if node == goal:
            return cost, path
        for child, step in graph.get(node, []):
            candidate = cost + step
            if candidate < best.get(child, float("inf")):
                best[child] = candidate
                item = (candidate, child, path + (child,))
                heapq.heappush(queue, item)
    return None

graph = {"start": [("A", 1), ("B", 3)],
         "A": [("goal", 9)], "B": [("goal", 2)], "goal": []}
expected = (5, ("start", "B", "goal"))
assert shortest(graph, "start", "goal") == expected
assert shortest(graph, "goal", "goal") == (0, ("goal",))
assert shortest(graph, "goal", "missing") is None
try:
    shortest({"a": [("b", -1)]}, "a", "b")
except ValueError:
    pass
else:
    raise AssertionError("отрицательное ребро принято")
print("Поиск: оптимальная цена 5, путь start → B → goal")
