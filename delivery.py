import json
from hashlib import sha256

class Mailbox:
    def __init__(self):
        self.seen = {}
        self.accepted = []

    def receive(self, event_id, payload):
        canonical = json.dumps(payload, sort_keys=True)
        digest = sha256(canonical.encode()).hexdigest()
        if event_id in self.seen:
            old_digest, receipt = self.seen[event_id]
            if old_digest != digest:
                raise ValueError('Конфликт содержимого события')
            return receipt
        receipt = "receipt-" + str(len(self.seen) + 1)
        self.accepted.append(payload)
        self.seen[event_id] = (digest, receipt)
        return receipt

box = Mailbox()
first = box.receive("e-1", {"task": "t-1"})
assert box.receive("e-1", {"task": "t-1"}) == first
assert len(box.accepted) == 1
try:
    box.receive("e-1", {"task": "t-2"})
except ValueError:
    print('Дубликаты и конфликты проверены')
else:
    raise AssertionError('Конфликт ошибочно принят')
