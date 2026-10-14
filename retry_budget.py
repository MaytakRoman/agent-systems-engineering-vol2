def schedule(attempts, initial, maximum):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("неверное число попыток")
    if initial <= 0 or maximum < initial:
        raise ValueError("неверные задержки")
    return [min(maximum, initial * 2**k)
            for k in range(attempts - 1)]

waits = schedule(5, 0.5, 4)
assert waits == [0.5, 1, 2, 4]
assert sum(waits) == 7.5
assert 5 * 2 + sum(waits) == 17.5
assert schedule(1, 0.5, 4) == []
for params in [(0, 0.5, 4), (2, -1, 4), (2, 4, 1)]:
    try:
        schedule(*params)
    except ValueError:
        pass
    else:
        raise AssertionError("неверный профиль принят")
print("Повторы: ожидание 7.5 с, верхняя оценка 17.5 с")
