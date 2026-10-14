def normalize(response):
    if type(response.get("complete")) is not bool:
        raise ValueError("нет признака полноты")
    items = []
    for row in response.get("rows", []):
        if not {"id", "version", "title"} <= set(row):
            raise ValueError("неполная запись")
        items.append({key: row[key]
                      for key in ("id", "version", "title")})
    return {"items": items,
            "complete": response["complete"],
            "next_cursor": response.get("next_cursor")}

result = normalize({"rows": [], "complete": False,
                    "next_cursor": "page-2"})
assert result["items"] == []
assert result["complete"] is False
assert result["next_cursor"] == "page-2"
full = normalize({"rows": [{"id": "D-1", "version": 3,
                             "title": "Инструкция",
                             "debug": 9}],
                  "complete": True})
assert "debug" not in full["items"][0]
assert full["complete"] is True
try:
    normalize({"rows": []})
except ValueError:
    pass
else:
    raise AssertionError("полнота потеряна")
print("Адаптер: неполный результат сохранён")
