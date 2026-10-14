durations = (4, 7, 5)
prices = (2, 3, 2)
dispatch = 2
merge = 3
serial = sum(durations) + merge
parallel = dispatch + max(durations) + merge
merge_cost = 2
orchestration = 1
cost_serial = sum(prices) + merge_cost
cost_parallel = sum(prices) + merge_cost + orchestration
assert serial == 19
assert parallel == 12
assert cost_serial == 9 and cost_parallel == 10
print('Последовательное время, с:', serial)
print('Параллельное время, с:', parallel)
print('Ускорение:', round(serial / parallel, 3))
print('Условные цены:', cost_serial, cost_parallel)
