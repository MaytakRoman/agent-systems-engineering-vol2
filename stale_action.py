class Page:
    def __init__(self):
        self.generation = 1
        self.object_version = 7
        self.value = "old"

    def observe(self):
        return self.generation, self.object_version

    def fill(self, expected, value):
        if expected != self.observe():
            raise ValueError('Устаревшее наблюдение')
        self.value = value
        self.generation += 1
        self.object_version += 1

page = Page()
old = page.observe()
page.fill(old, "first")
try:
    page.fill(old, "wrong")
except ValueError:
    pass
else:
    raise AssertionError('Устаревшее действие ошибочно принято')
page.fill(page.observe(), "verified")
assert page.value == "verified"
print('Устаревшее действие отклонено; обновление принято')
