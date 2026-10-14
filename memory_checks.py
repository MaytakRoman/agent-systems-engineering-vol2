def route(event):
    if event.get("policy_request"):
        return "reject_policy_change"
    if event.get("unknown"):
        return "reconcile"
    if not event.get("permission", True):
        return "stop_write"
    if event.get("source_changed"):
        return "reread"
    return "continue"

cases = [
    ({}, "continue"),
    ({"source_changed": True}, "reread"),
    ({"unknown": "i-1"}, "reconcile"),
    ({"permission": False}, "stop_write"),
    ({"policy_request": True}, "reject_policy_change"),
    ({"unknown": "i-2", "source_changed": True},
     "reconcile"),
    ({"permission": False, "source_changed": True},
     "stop_write"),
    ({"source_changed": False}, "continue"),
]
for event, expected in cases:
    assert route(event) == expected
print(f'Сценарии памяти: {len(cases)}, проверка пройдена')
