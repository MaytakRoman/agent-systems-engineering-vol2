from hashlib import sha256

def accept(assignment, result, content):
    if result["task"] != assignment["task"]:
        return "wrong_task"
    if result["generation"] != assignment["generation"]:
        return "obsolete"
    if result["inputs"] != assignment["inputs"]:
        return "input_conflict"
    if result["status"] != "ready":
        return "not_ready"
    if sha256(content).hexdigest() != result["hash"]:
        return "artifact_conflict"
    if not result["evidence"]:
        return "missing_evidence"
    return "accepted"

assignment = dict(task="t1", generation=3,
                  inputs={"manual": 5})
data = b"limit=80; unit=C; mode=normal"
result = dict(task="t1", generation=3,
              inputs={"manual": 5}, status="ready",
              hash=sha256(data).hexdigest(),
              evidence=["manual:5:page12"])
assert accept(assignment, result, data) == "accepted"
result["generation"] = 2
assert accept(assignment, result, data) == "obsolete"
print('Проверка передачи пройдена')
