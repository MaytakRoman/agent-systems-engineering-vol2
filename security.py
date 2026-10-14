from dataclasses import replace
from framework import (
    example_components, Proposal, Confirmation, Denied, Conflict, Gate)
import json


class GateWithoutRecipient(Gate):
    def check_recipient(self, proposal, profile):
        pass  # Намеренно отключён только контроль адресата.


def run():
    good = Proposal("I1", "T-1", 1, "I-1", 3,
                    "P-1", "internal", "учебный отчёт")
    cases = [good, replace(good, recipient="external"),
             replace(good, object_id="closed"),
             replace(good, operation="delete"),
             replace(good, source_revision=2),
             replace(good, equipment="P-2")]
    allowed = blocked = 0
    for proposal in cases:
        agent, store, _ = example_components()
        confirmation = Confirmation(
            "reviewer", proposal.package_hash(), 100)
        try:
            store.commit(proposal, lambda: agent.gate.check(
                proposal, agent.profile, confirmation, 0))
        except (Denied, Conflict):
            blocked += 1
            assert store.count() == 0
        else:
            allowed += 1
            assert store.count() == 1
        finally:
            store.close()
    agent, store, _ = example_components()
    agent.gate = GateWithoutRecipient(agent.catalog)
    unsafe = cases[1]
    confirmation = Confirmation("reviewer", unsafe.package_hash(), 100)
    store.commit(unsafe, lambda: agent.gate.check(
        unsafe, agent.profile, confirmation, 0))
    unauthorized = store.count()
    assert store.payload(unsafe.intent_id)["recipient"] == "external"
    assert (allowed, blocked, unauthorized) == (1, 5, 1)
    store.close()
    return {"proposals": 6, "lawful_allowed": allowed,
            "forbidden_blocked": blocked,
            "negative_control_unauthorized": unauthorized}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
