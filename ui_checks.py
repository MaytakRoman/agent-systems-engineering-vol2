from ui_model import Form

form = Form()
form.fill(0, "equipment", "unit-A")
form.fill(1, "description", "bearing noise")
old_version = form.read()[0]
result = form.submit(old_version, "intent-1")
# Клиент считает ответ потерянным.
recovered = form.reconcile("intent-1")
assert recovered["id"] == result["id"]
assert form.submit(old_version, "intent-1") == result
assert len(form.sent) == 1

version, fields = form.read()
form.fill(version, "description", "updated symptom")
try:
    form.fill(version, "description", "stale edit")
except ValueError:
    pass
else:
    raise AssertionError('Устаревшее изменение ошибочно принято')
form.fill(form.read()[0], "description", "checked")
assert form.read()[1]["description"] == "checked"
assert form.sent["intent-1"]["fields"] == fields
print('Интерфейс: согласование, дедупликация и конфликт проверены')
