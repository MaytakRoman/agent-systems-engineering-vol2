def process(rows):
    totals = {}
    errors = []
    for number, row in enumerate(rows):
        try:
            code = row["code"]
            quantity = row["quantity"]
            totals[code] = totals.get(code, 0) + quantity
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError('Недопустимое количество')
            if not isinstance(code, str) or not code.strip():
                raise ValueError('Недопустимый код')
        except (KeyError, TypeError, ValueError):
            errors.append(number)
    return totals, errors

if __name__ == "__main__":
    rows = [dict(code="A", quantity=2),
            dict(code="A", quantity=-1)]
    totals, errors = process(rows)
    assert totals == {"A": 1}  # Наблюдаемый дефект
    assert errors == [1]
    print('До исправления: воспроизведён частичный эффект')
