import hashlib
import json


def fingerprint(args):
    """Допустить только объект с простыми скалярными полями."""
    allowed = (str, int, bool, type(None))
    if type(args) is not dict:
        raise ValueError("нужен объект")
    if any(type(key) is not str for key in args):
        raise ValueError("ключ должен быть строкой")
    if any(type(value) not in allowed
           for value in args.values()):
        raise ValueError("тип вне локального профиля")
    encoded = json.dumps(
        args, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

a = {"request_id": "REQ-7", "version": 12, "text": "проект"}
b = {"text": "проект", "version": 12, "request_id": "REQ-7"}
assert fingerprint(a) == fingerprint(b)
assert fingerprint(a) != fingerprint(dict(a, version=13))
try:
    fingerprint({"amount": 0.5})
except ValueError:
    pass
else:
    raise AssertionError("тип вне профиля принят")
print("Отпечаток: порядок ключей не влияет")
