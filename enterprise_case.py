from framework import (
    example_components, Task, Confirmation, Status)
import json


def run():
    counts = {"accepted": 0, "need_info": 0, "rejected": 0}
    cases = ["normal", "missing", "inactive", "conflict", "recipient"]
    for case in cases:
        agent, store, _ = example_components()
        task = Task(case, "T-1", "" if case == "missing" else "P-1")
        agent.prepare(task, "external" if case == "recipient" else "internal")
        if task.status == Status.NEED_INFO:
            counts["need_info"] += 1
            store.close()
            continue
        if case == "inactive":
            from dataclasses import replace
            source = agent.catalog.sources["I-1"]
            agent.catalog.sources["I-1"] = replace(source, active=False)
        if case == "conflict":
            with store.db:
                store.db.execute("UPDATE objects SET version=2")
        confirmation = Confirmation(
            "reviewer", task.proposal.package_hash(), 100)
        agent.execute(task, confirmation)
        counts[task.status.value] += 1
        assert store.count() == int(case == "normal")
        store.close()
    assert counts == {"accepted": 1, "need_info": 1, "rejected": 3}
    return counts


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
