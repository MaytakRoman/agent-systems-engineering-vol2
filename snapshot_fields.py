from copy import deepcopy

REQUIRED = {"goal", "goal_version", "inputs",
            "constraints", "unknown", "artifacts"}

def checkpoint(old, candidate):
    if not REQUIRED <= candidate.keys():
        raise ValueError('Отсутствуют обязательные поля')
    for key in ("goal", "goal_version", "constraints"):
        if candidate[key] != old[key]:
            raise ValueError('Изменено защищённое поле')
    if candidate["unknown"] != old["unknown"]:
        raise ValueError('Утрачен неизвестный исход')
    for name, version in old["inputs"].items():
        if candidate["inputs"].get(name) != version:
            raise ValueError('Изменена версия входа')
    return deepcopy(candidate)

old = dict(goal="report", goal_version=2,
           inputs={"manual": 5},
           constraints=["draft only"],
           unknown=["intent-7"], artifacts=["a-1"])
candidate = deepcopy(old)
candidate["note"] = "continue after reconciliation"
assert checkpoint(old, candidate)["goal_version"] == 2
candidate["unknown"] = []
try:
    checkpoint(old, candidate)
except ValueError:
    print('Защищённый исход сохранён')
else:
    raise AssertionError('Утрата ошибочно принята')
