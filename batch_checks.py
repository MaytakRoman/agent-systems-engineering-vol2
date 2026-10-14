from batch_before import process as before
from batch_after import process as after

def check_partial_effect(fn):
    rows = [dict(code="A", quantity=2),
            dict(code="A", quantity=-1)]
    totals, errors = fn(rows)
    assert totals == {"A": 2}
    assert errors == [1]

def check_all(fn):
    cases = [
        ([dict(code="A", quantity=2)], ({"A": 2}, [])),
        ([dict(code="A", quantity=2),
          dict(code="A", quantity=3)], ({"A": 5}, [])),
    ]
    for invalid in (-1, 0, True, "2"):
        rows = [dict(code="A", quantity=invalid),
                dict(code="B", quantity=3)]
        cases.append((rows, ({"B": 3}, [0])))
    cases.append(([dict(code="", quantity=1)], ({}, [0])))
    for rows, expected in cases:
        assert fn(rows) == expected
    check_partial_effect(fn)
    return len(cases) + 1

try:
    check_partial_effect(before)
except AssertionError:
    print('Отрицательный контроль: дефект выявлен')
else:
    raise AssertionError('Тест пропускает исходный дефект')
print(f'После исправления: {check_all(after)}, проверки пройдены')
