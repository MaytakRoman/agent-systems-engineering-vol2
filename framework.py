'Конечный учебный агент без сети и внешних эффектов.'
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
from typing import Callable
import json
import sqlite3


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False,
                      sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return sha256(canonical(value).encode("utf-8")).hexdigest()


class Status(str, Enum):
    NEW = "new"
    NEED_INFO = "need_info"
    PREPARED = "prepared"
    WAIT_CONFIRM = "wait_confirm"
    NOT_SENT = "not_sent"
    UNKNOWN = "unknown"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Denied(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class Conflict(Exception):
    pass


class LostReply(Exception):
    pass


class TransientFailure(Exception):
    """Вызов прерван до отправки; предметный эффект отсутствует."""
    pass


@dataclass(frozen=True)
class Source:
    object_id: str
    revision: int
    active: bool
    equipment: str
    text: str


@dataclass(frozen=True)
class Proposal:
    intent_id: str
    object_id: str
    expected_version: int
    source_id: str
    source_revision: int
    equipment: str
    recipient: str
    body: str
    operation: str = "publish"

    def package_hash(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class Confirmation:
    actor: str
    package_hash: str
    expires: int


@dataclass(frozen=True)
class Profile:
    actor: str
    operations: frozenset[str]
    objects: frozenset[str]
    recipients: frozenset[str]


@dataclass(frozen=True)
class Receipt:
    intent_id: str
    object_id: str
    version: int
    package_hash: str
    record_id: int


@dataclass
class Task:
    task_id: str
    object_id: str
    equipment: str
    status: Status = Status.NEW
    proposal: Proposal | None = None
    receipt: Receipt | None = None
    reason: str = ""


class Catalog:
    def __init__(self, sources: list[Source]):
        self.sources = {s.object_id: s for s in sources}

    def read(self, source_id: str) -> Source:
        if source_id not in self.sources:
            raise Denied("source_missing")
        return self.sources[source_id]

    def current(self, equipment: str) -> Source:
        candidates = [s for s in self.sources.values()
                      if s.equipment == equipment and s.active]
        if len(candidates) != 1:
            raise Denied("ambiguous_or_missing_source")
        return candidates[0]


class Gate:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def check_recipient(self, proposal, profile):
        if proposal.recipient not in profile.recipients:
            raise Denied("recipient")

    def check(self, proposal: Proposal, profile: Profile,
              confirmation: Confirmation | None,
              now: int) -> None:
        if proposal.operation not in profile.operations:
            raise Denied("operation")
        if proposal.object_id not in profile.objects:
            raise Denied("object_scope")
        self.check_recipient(proposal, profile)
        source = self.catalog.read(proposal.source_id)
        if not source.active:
            raise Denied("inactive_source")
        if source.revision != proposal.source_revision:
            raise Conflict("source_revision")
        if source.equipment != proposal.equipment:
            raise Denied("equipment_mismatch")
        if not proposal.body.strip():
            raise Denied("empty_body")
        if confirmation is None:
            raise Denied("confirmation_missing")
        if confirmation.actor != profile.actor:
            raise Denied("confirmation_actor")
        if confirmation.expires < now:
            raise Denied("confirmation_expired")
        if confirmation.package_hash != proposal.package_hash():
            raise Denied("confirmation_package")


class Store:
    'Локальный транзакционный сервис с дедупликацией намерений.'
    def __init__(self, path: str = ":memory:"):
        self.db = sqlite3.connect(path)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS objects (
          object_id TEXT PRIMARY KEY, version INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS effects (
          record_id INTEGER PRIMARY KEY,
          intent_id TEXT UNIQUE NOT NULL,
          object_id TEXT NOT NULL,
          version INTEGER NOT NULL,
          package_hash TEXT NOT NULL,
          payload TEXT NOT NULL);
        """)
        self.db.commit()

    def seed(self, object_id: str, version: int = 1) -> None:
        with self.db:
            self.db.execute(
                "INSERT INTO objects VALUES (?, ?)",
                (object_id, version))

    def version(self, object_id: str) -> int:
        row = self.db.execute(
            "SELECT version FROM objects WHERE object_id=?",
            (object_id,)).fetchone()
        if row is None:
            raise Denied("object_missing")
        return int(row[0])

    def receipt(self, intent_id: str) -> Receipt | None:
        row = self.db.execute("""
          SELECT intent_id, object_id, version,
                 package_hash, record_id FROM effects
          WHERE intent_id=?
        """, (intent_id,)).fetchone()
        return Receipt(*row) if row is not None else None

    def count(self) -> int:
        return int(self.db.execute(
            "SELECT COUNT(*) FROM effects").fetchone()[0])

    def payload(self, intent_id: str) -> dict:
        row = self.db.execute(
            "SELECT payload FROM effects WHERE intent_id=?",
            (intent_id,)).fetchone()
        if row is None:
            raise Denied("effect_missing")
        return json.loads(row[0])

    def commit(self, proposal: Proposal,
               authorize: Callable[[], None],
               lose_reply: bool = False) -> Receipt:
        try:
            self.db.execute("BEGIN IMMEDIATE")
            authorize()
            old = self.receipt(proposal.intent_id)
            if old is not None:
                if old.package_hash != proposal.package_hash():
                    raise Conflict("intent_payload_changed")
                self.db.commit()
                return old
            current = self.version(proposal.object_id)
            if current != proposal.expected_version:
                raise Conflict("object_version")
            next_version = current + 1
            cursor = self.db.execute("""
              INSERT INTO effects
              (intent_id, object_id, version,
               package_hash, payload) VALUES (?, ?, ?, ?, ?)
            """, (proposal.intent_id, proposal.object_id,
                  next_version, proposal.package_hash(),
                  canonical(asdict(proposal))))
            self.db.execute("""
              UPDATE objects SET version=? WHERE object_id=?
            """, (next_version, proposal.object_id))
            receipt = Receipt(
                proposal.intent_id, proposal.object_id,
                next_version, proposal.package_hash(),
                int(cursor.lastrowid))
            self.db.commit()
        except Exception:
            if self.db.in_transaction:
                self.db.rollback()
            raise
        if lose_reply:
            raise LostReply("committed_without_reply")
        return receipt

    def close(self) -> None:
        self.db.close()


class Audit:
    def __init__(self):
        self.events: list[dict] = []
        self.head = "0" * 64

    def append(self, event: dict) -> None:
        event = json.loads(canonical(event))
        row = {"previous": self.head, "event": event}
        row["hash"] = digest(row)
        self.events.append(row)
        self.head = row["hash"]

    def verify(self, trusted_head: str) -> bool:
        previous = "0" * 64
        for row in self.events:
            content = {"previous": row["previous"],
                       "event": row["event"]}
            if row["previous"] != previous:
                return False
            if row["hash"] != digest(content):
                return False
            previous = row["hash"]
        return previous == trusted_head


class Acceptor:
    def __init__(self, store: Store, catalog: Catalog):
        self.store = store
        self.catalog = catalog

    def check(self, proposal: Proposal,
              receipt: Receipt) -> bool:
        observed = self.store.receipt(proposal.intent_id)
        if observed != receipt:
            return False
        if receipt.package_hash != proposal.package_hash():
            return False
        if self.store.payload(proposal.intent_id) != asdict(proposal):
            return False
        source = self.catalog.read(proposal.source_id)
        return (source.active
                and source.revision == proposal.source_revision
                and source.equipment == proposal.equipment)


class Agent:
    def __init__(self, catalog: Catalog, store: Store,
                 profile: Profile, audit: Audit):
        self.catalog = catalog
        self.store = store
        self.profile = profile
        self.audit = audit
        self.gate = Gate(catalog)
        self.acceptor = Acceptor(store, catalog)

    def prepare(self, task: Task, recipient: str) -> None:
        if not task.equipment:
            task.status = Status.NEED_INFO
            task.reason = "equipment_required"
            return
        try:
            source = self.catalog.current(task.equipment)
        except Denied as error:
            task.status = Status.NEED_INFO
            task.reason = str(error)
            self.audit.append({"task": task.task_id,
                               "event": task.status.value,
                               "reason": task.reason})
            return
        try:
            expected = self.store.version(task.object_id)
        except Denied as error:
            task.status = Status.REJECTED
            task.reason = str(error)
            self.audit.append({"task": task.task_id,
                               "event": task.status.value,
                               "reason": task.reason})
            return
        task.proposal = Proposal(
            intent_id=task.task_id + ":publish:1",
            object_id=task.object_id,
            expected_version=expected,
            source_id=source.object_id,
            source_revision=source.revision,
            equipment=task.equipment,
            recipient=recipient,
            body="Draft based on " + source.object_id)
        task.status = Status.WAIT_CONFIRM
        self.audit.append({"task": task.task_id,
                           "event": "prepared",
                           "hash": task.proposal.package_hash()})

    def execute(self, task: Task,
                confirmation: Confirmation,
                now: int = 0, lose_reply: bool = False) -> None:
        if task.proposal is None:
            raise Denied("proposal_missing")
        proposal = task.proposal
        authorize = lambda: self.gate.check(
            proposal, self.profile, confirmation, now)
        try:
            receipt = self.store.commit(
                proposal, authorize, lose_reply)
        except TransientFailure:
            task.status = Status.NOT_SENT
            task.reason = "not_sent"
            self.audit.append({"task": task.task_id,
                               "event": "not_sent",
                               "intent": proposal.intent_id})
            return
        except LostReply:
            task.status = Status.UNKNOWN
            task.reason = "reply_lost"
            self.audit.append({"task": task.task_id,
                               "event": "unknown",
                               "intent": proposal.intent_id})
            return
        except (Denied, Conflict) as error:
            if (isinstance(error, Denied)
                    and error.code == "confirmation_expired"
                    and proposal.object_id in self.profile.objects):
                old = self.store.receipt(proposal.intent_id)
                if (old is not None
                        and old.package_hash == proposal.package_hash()):
                    self.finish(task, old)
                    return
            task.status = Status.REJECTED
            task.reason = str(error)
            self.audit.append({"task": task.task_id,
                               "event": "rejected",
                               "reason": task.reason})
            return
        self.finish(task, receipt)

    def finish(self, task: Task, receipt: Receipt) -> None:
        if task.proposal is None:
            raise Denied("proposal_missing")
        task.receipt = receipt
        accepted = self.acceptor.check(task.proposal, receipt)
        task.status = (Status.ACCEPTED if accepted
                       else Status.REJECTED)
        task.reason = "" if accepted else "acceptance_failed"
        self.audit.append({"task": task.task_id,
                           "event": task.status.value,
                           "receipt": asdict(receipt)})

    def reconcile(self, task: Task) -> None:
        if task.proposal is None:
            raise Denied("proposal_missing")
        receipt = self.store.receipt(task.proposal.intent_id)
        if receipt is None:
            task.status = Status.UNKNOWN
            task.reason = "no_receipt_requires_review"
            return
        self.finish(task, receipt)


def example_components():
    catalog = Catalog([Source("I-1", 3, True, "P-1", "Manual")])
    store = Store()
    store.seed("T-1")
    profile = Profile("reviewer", frozenset({"publish"}),
                      frozenset({"T-1"}),
                      frozenset({"internal"}))
    audit = Audit()
    return Agent(catalog, store, profile, audit), store, audit


if __name__ == "__main__":
    agent, store, audit = example_components()
    task = Task("job-1", "T-1", "P-1")
    agent.prepare(task, "internal")
    confirmation = Confirmation(
        "reviewer", task.proposal.package_hash(), 100)
    agent.execute(task, confirmation, lose_reply=True)
    assert task.status == Status.UNKNOWN
    agent.reconcile(task)
    assert task.status == Status.ACCEPTED
    assert store.count() == 1
    assert audit.verify(audit.head)
    print('Принято после согласования; эффектов: 1')
    store.close()
