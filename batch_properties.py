from itertools import product
from batch_after import process

alphabet = (
    {"code": "A", "quantity": 1},
    {"code": "A", "quantity": 2},
    {"code": "B", "quantity": 3},
    {"code": "A", "quantity": -1},
    {"code": "A", "quantity": True},
    {"code": "", "quantity": 2},
)

def reference(rows):
    valid = []
    errors = []
    for index, row in enumerate(rows):
        code, value = row["code"], row["quantity"]
        if (type(value) is int and value > 0
            and isinstance(code, str) and code.strip()):
            valid.append((code, value))
        else:
            errors.append(index)
    totals = {}
    for code in {x[0] for x in valid}:
        totals[code] = sum(v for c, v in valid if c == code)
    return totals, errors

tested = 0
for length in range(4):
    for rows in product(alphabet, repeat=length):
        assert process(rows) == reference(rows)
        assert process(rows)[0] == process(rows[::-1])[0]
        middle = len(rows) // 2
        left, _ = process(rows[:middle])
        right, _ = process(rows[middle:])
        merged = dict(left)
        for code, value in right.items():
            merged[code] = merged.get(code, 0) + value
        assert merged == process(rows)[0]
        tested += 1
assert tested == 259
print(f'Пакетов проверено: {tested}; эталон, порядок и разбиение согласованы')
