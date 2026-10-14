from copy import deepcopy
from framework import Audit

audit = Audit()
audit.append({"event": "proposal", "task": "J1"})
audit.append({"event": "accepted", "task": "J1"})
trusted = audit.head
assert audit.verify(trusted)
original = deepcopy(audit.events)
audit.events[0]["event"]["task"] = "J2"
assert not audit.verify(trusted)
audit.events = deepcopy(original)
audit.events.pop()
assert not audit.verify(trusted)
audit.events = original
assert audit.verify(trusted)
print('Изменение и усечение выявлены по доверенному концу цепочки')
