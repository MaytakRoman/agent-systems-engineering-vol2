def transform(point, origin, scale, bounds):
    x = origin[0] + scale[0] * point[0]
    y = origin[1] + scale[1] * point[1]
    left, top, right, bottom = bounds
    if not (left <= x < right and top <= y < bottom):
        raise ValueError('Вне области интерфейса')
    return x, y

assert transform((100, 50), (20, 30), (2, 2),
                 (20, 30, 820, 630)) == (220, 130)
try:
    transform((500, 50), (20, 30), (2, 2),
              (20, 30, 820, 630))
except ValueError:
    print('Преобразование координат и границы проверены')
else:
    raise AssertionError('Действие вне области ошибочно принято')
