from dataclasses import replace
from framework import (
    example_components, Task, Confirmation, Status, Conflict,
    Store, Receipt)


def accepted_task():
    agent, store, audit = example_components()
    task = Task("J1", "T-1", "P-1")
    agent.prepare(task, "internal")
    c = Confirmation("reviewer", task.proposal.package_hash(), 100)
    agent.execute(task, c)
    assert task.status == Status.ACCEPTED
    return agent, store, task, c


agent, store, task, c = accepted_task()
agent.execute(task, c)
assert store.count() == 1
changed = replace(task.proposal, body="changed")
new_confirmation = Confirmation("reviewer", changed.package_hash(), 100)
try:
    store.commit(changed, lambda: agent.gate.check(
        changed, agent.profile, new_confirmation, 0))
except Conflict:
    pass
else:
    raise AssertionError('Принято изменённое намерение')
assert store.count() == 1
store.close()

agent, store, audit = example_components()
task = Task("J2", "T-1", "P-1")
agent.prepare(task, "internal")
c = Confirmation("reviewer", task.proposal.package_hash(), 100)
agent.execute(task, c, lose_reply=True)
assert task.status == Status.UNKNOWN
agent.reconcile(task)
assert task.status == Status.ACCEPTED
assert store.count() == 1
store.close()

# Дефектный сервис повторно фиксирует уже зарегистрированный эффект.
class StoreWithoutDeduplication(Store):
    def __init__(self):
        super().__init__()
        sql = self.db.execute(
            "SELECT sql FROM sqlite_master WHERE name='effects'").fetchone()[0]
        self.db.execute("DROP TABLE effects")
        self.db.execute(sql.replace("UNIQUE NOT NULL", "NOT NULL"))
        self.db.commit()

    def commit(self, proposal, authorize, lose_reply=False):
        old = self.receipt(proposal.intent_id)
        if old is None:
            return super().commit(proposal, authorize, lose_reply)
        # Ошибка: вместо возврата свидетельства создаётся новая запись.
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            authorize()
            cursor = self.db.execute("""
              INSERT INTO effects
              (intent_id, object_id, version, package_hash, payload)
              SELECT intent_id, object_id, version, package_hash, payload
              FROM effects WHERE record_id=?
            """, (old.record_id,))
            return Receipt(old.intent_id, old.object_id, old.version,
                           old.package_hash, int(cursor.lastrowid))


agent, ordinary, _ = example_components()
ordinary.close()
unsafe = StoreWithoutDeduplication()
unsafe.seed("T-1")
agent.store = unsafe
task = Task("J3", "T-1", "P-1")
agent.prepare(task, "internal")
proposal = task.proposal
c = Confirmation("reviewer", proposal.package_hash(), 100)
authorize = lambda: agent.gate.check(proposal, agent.profile, c, 0)
unsafe.commit(proposal, authorize)
unsafe.commit(proposal, authorize)
assert unsafe.count() == 2
assert unsafe.db.execute(
    "SELECT COUNT(DISTINCT intent_id) FROM effects").fetchone()[0] == 1
unsafe.close()

# Истёкшее подтверждение запрещает новую запись, но допускает чтение прошлого.
agent, store, task, c = accepted_task()
agent.execute(task, c, now=101)
assert task.status == Status.ACCEPTED and store.count() == 1
store.close()
agent, store, _ = example_components()
task = Task("J4", "T-1", "P-1")
agent.prepare(task, "internal")
c = Confirmation("reviewer", task.proposal.package_hash(), 100)
agent.execute(task, c, now=101)
assert task.status == Status.REJECTED and store.count() == 0
missing = Task("J5", "T-1", "P-404")
agent.prepare(missing, "internal")
assert missing.status == Status.NEED_INFO and missing.reason
store.close()
print("Повтор, конфликт, восстановление и отрицательный контроль: пройдены")
