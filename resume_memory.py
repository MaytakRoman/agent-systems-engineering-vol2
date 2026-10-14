class LocalStore:
    def __init__(self):
        self.results = {}
        self.effects = 0

    def save(self, intent, text, lose_reply=False):
        """Вернуть старый результат или создать эффект."""
        if intent in self.results:
            old_text, result = self.results[intent]
            if old_text != text:
                raise ValueError("конфликт намерения")
            return result
        self.effects += 1
        result = {"draft_id": self.effects, "saved": True}
        self.results[intent] = (text, result)
        if lose_reply:
            raise TimeoutError("ответ потерян после записи")
        return result

store = LocalStore()
try:
    store.save("I-1", "проект", lose_reply=True)
except TimeoutError:
    pass
assert store.effects == 1
result = store.save("I-1", "проект")
assert result["draft_id"] == 1
assert store.effects == 1
try:
    store.save("I-1", "иной проект")
except ValueError:
    pass
else:
    raise AssertionError("изменение аргументов принято")
print("Возобновление: один эффект и конфликт обнаружен")
