import json

class ProgressGuard:
    def __init__(self, limit=2):
        self.limit = limit
        self.counts = {}

    def allow(self, operation, arguments, snapshot):
        key = (operation, snapshot,
               json.dumps(arguments, sort_keys=True))
        count = self.counts.get(key, 0)
        if count >= self.limit:
            return False
        self.counts[key] = count + 1
        return True

guard = ProgressGuard()
args = {"request": "REQ-7"}
assert guard.allow("read", args, 12)
assert guard.allow("read", args, 12)
assert not guard.allow("read", args, 12)
assert guard.allow("read", args, 13)
assert guard.allow("metadata", args, 12)
print("Прогресс: повтор ограничен, новый снимок разрешён")
