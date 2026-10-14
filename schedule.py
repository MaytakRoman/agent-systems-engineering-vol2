def makespan(durations, workers):
    if workers < 1:
        raise ValueError('Число исполнителей')
    free_at = [0] * workers
    assignments = []
    for task, duration in enumerate(durations):
        slot = min(range(workers), key=free_at.__getitem__)
        start = free_at[slot]
        free_at[slot] += duration
        assignments.append((task, slot, start,
                            free_at[slot]))
    return max(free_at, default=0), assignments

normal = (4, 7, 5)
slow = (4, 15, 5)
for values in (normal, slow):
    times = [makespan(values, n)[0] for n in (1, 2, 3)]
    assert times[2] <= times[1] <= times[0]
    print('Длительности:', values, 'Время:', times)
assert makespan(normal, 2)[0] == 9
assert makespan(normal, 3)[0] == 7
