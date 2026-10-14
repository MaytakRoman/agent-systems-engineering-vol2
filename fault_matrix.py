from framework import (
    example_components, Task, Confirmation, Status, TransientFailure, Store)


class FailBeforeCommit(Store):
    def __init__(self):
        super().__init__()
        self.fail_once = True

    def commit(self, proposal, authorize, lose_reply=False):
        if self.fail_once:
            self.fail_once = False
            raise TransientFailure("отказ до отправки")
        return super().commit(proposal, authorize, lose_reply)


for fault in ("before", "after_commit", "none"):
    agent, store, audit = example_components()
    if fault == "before":
        store.close()
        store = FailBeforeCommit()
        store.seed("T-1")
        agent.store = store
        agent.acceptor.store = store
    task = Task("J1", "T-1", "P-1")
    agent.prepare(task, "internal")
    confirmation = Confirmation(
        "reviewer", task.proposal.package_hash(), 100)
    agent.execute(task, confirmation,
                  lose_reply=fault == "after_commit")
    if fault == "before":
        assert task.status == Status.NOT_SENT and store.count() == 0
        agent.execute(task, confirmation)
    elif fault == "after_commit":
        assert task.status == Status.UNKNOWN and store.count() == 1
        agent.reconcile(task)
    assert task.status == Status.ACCEPTED
    agent.execute(task, confirmation)
    assert store.count() == 1
    assert audit.verify(audit.head)
    store.close()
print("Две точки отказа, базовый сценарий и три повтора: пройдены")
