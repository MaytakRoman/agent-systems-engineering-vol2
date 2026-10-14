class Form:
    def __init__(self):
        self.version = 0
        self.fields = {}
        self.sent = {}
        self.intent_versions = {}

    def read(self):
        return self.version, dict(self.fields)

    def fill(self, version, name, value):
        if version != self.version:
            raise ValueError('Конфликт версии')
        self.fields[name] = value
        self.version += 1

    def submit(self, version, intent):
        if intent in self.sent:
            if version != self.intent_versions[intent]:
                raise ValueError('Конфликт версии намерения')
            return self.sent[intent]
        if version != self.version:
            raise ValueError('Конфликт версии')
        if not all(self.fields.get(k)
                   for k in ("equipment", "description")):
            raise ValueError('Неполная форма')
        result = dict(id="request-" + str(len(self.sent)+1),
                      fields=dict(self.fields))
        self.sent[intent] = result
        self.intent_versions[intent] = version
        self.version += 1
        return result

    def reconcile(self, intent):
        return self.sent.get(intent)

if __name__ == "__main__":
    form = Form()
    assert form.read() == (0, {})
    print('Модель формы готова')
