def validate(args):
    """Проверить локальный профиль без полного JSON Schema."""
    if type(args) is not dict:
        raise ValueError("ожидается объект")
    keys = {"request_id", "version", "text"}
    if set(args) != keys:
        raise ValueError("неверный набор полей")
    if not isinstance(args["request_id"], str):
        raise ValueError("неверный тип идентификатора")
    if not args["request_id"].startswith("REQ-"):
        raise ValueError("неверный идентификатор")
    if type(args["version"]) is not int:
        raise ValueError("версия должна быть целой")
    if args["version"] < 0:
        raise ValueError("отрицательная версия")
    if not isinstance(args["text"], str):
        raise ValueError("текст должен быть строкой")
    if not 1 <= len(args["text"]) <= 2000:
        raise ValueError("недопустимая длина")
    return dict(args)

good = {"request_id": "REQ-7", "version": 12,
        "text": "проект"}
assert validate(good) == good
bad = [dict(good, version=True), dict(good, version=-1),
       dict(good, text=""), dict(good, unknown=1)]
for args in bad:
    try:
        validate(args)
    except ValueError:
        pass
    else:
        raise AssertionError("неверный запрос принят")
print("Схема: 5/5 проверок")
