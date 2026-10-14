def affected(dependencies, changed):
    known = set(dependencies)
    if not set(changed) <= known:
        raise ValueError("неизвестный изменённый объект")
    result = set(changed)
    while True:
        added = {node for node, pred in dependencies.items()
                 if set(pred) & result}
        updated = result | added
        if updated == result:
            return result
        result = updated

graph = {"request": [], "manual": [], "history": ["request"],
         "analysis": ["request", "manual", "history"],
         "draft": ["analysis"], "save": ["draft"]}
result = affected(graph, {"request"})
expected = {"request", "history", "analysis",
            "draft", "save"}
assert result == expected
assert "manual" not in result
assert affected(graph, set()) == set()
assert affected(graph, {"save"}) == {"save"}
print("Аннулированы:", sorted(result))
