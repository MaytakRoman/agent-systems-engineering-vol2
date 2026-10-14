def process(rows):
    totals = {}
    errors = []
    for number, row in enumerate(rows):
        try:
            code = row["code"]
            quantity = row["quantity"]
            if not isinstance(code, str) or not code.strip():
                raise ValueError('Недопустимый код')
            if type(quantity) is not int or quantity <= 0:
                raise ValueError('Недопустимое количество')
        except (KeyError, TypeError, ValueError):
            errors.append(number)
            continue
        totals[code] = totals.get(code, 0) + quantity
    return totals, errors

if __name__ == "__main__":
    rows = [dict(code="A", quantity=2),
            dict(code="A", quantity=-1)]
    totals, errors = process(rows)
    assert totals == {"A": 2}
    assert errors == [1]
    print('После исправления: атомарность строки сохранена')
