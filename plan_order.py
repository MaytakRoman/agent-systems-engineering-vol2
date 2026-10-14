from collections import deque


def order(dependencies):
    nodes = set(dependencies)
    if any(not set(pred) <= nodes
           for pred in dependencies.values()):
        raise ValueError("неизвестная зависимость")
    degree = {node: len(set(pred))
              for node, pred in dependencies.items()}
    ready = deque(sorted(node for node in nodes
                         if degree[node] == 0))
    result = []
    while ready:
        node = ready.popleft()
        result.append(node)
        for child in sorted(nodes):
            if node in dependencies[child]:
                degree[child] -= 1
                if degree[child] == 0:
                    ready.append(child)
    if len(result) != len(nodes):
        raise ValueError("цикл зависимостей")
    return result

graph = {"identify": [], "manual": ["identify"],
         "history": ["identify"],
         "draft": ["manual", "history"], "save": ["draft"]}
result = order(graph)
positions = {node: i for i, node in enumerate(result)}
assert all(positions[p] < positions[n]
           for n, preds in graph.items() for p in preds)
assert order({}) == []
try:
    order({"a": ["b"], "b": ["a"]})
except ValueError:
    pass
else:
    raise AssertionError("цикл пропущен")
print("Граф:", result)
