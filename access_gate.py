from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    operation: str
    object_id: str
    expected_version: int

@dataclass(frozen=True)
class Profile:
    object_id: str
    operations: frozenset


def admit(proposal, profile, current_version):
    """Проверить допуск без доверия к заявлению модели."""
    if proposal.object_id != profile.object_id:
        raise PermissionError("чужой объект")
    if proposal.operation not in profile.operations:
        raise PermissionError("операция запрещена")
    if proposal.expected_version != current_version:
        raise ValueError("конфликт версии")
    return proposal

profile = Profile("REQ-7", frozenset({"save_draft"}))
good = Proposal("save_draft", "REQ-7", 12)
assert admit(good, profile, 12) == good
cases = [
    (Proposal("save_draft", "REQ-8", 12), PermissionError),
    (Proposal("publish", "REQ-7", 12), PermissionError),
    (Proposal("save_draft", "REQ-7", 11), ValueError),
]
for proposal, error in cases:
    try:
        admit(proposal, profile, 12)
    except error:
        pass
    else:
        raise AssertionError("запрет не сработал")
print("Допуск: 4/4 проверки")
