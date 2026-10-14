'Табличная проверка покрытия демонстрациями без обучения языковой модели.'
from collections import Counter, defaultdict
import json

EXPERT = {"start": "read", "known": "draft",
          "missing": "ask", "recovery": "refresh"}
INITIAL = [("start", "read"), ("known", "draft"),
           ("missing", "ask")]


def fit(pairs):
    counts = defaultdict(Counter)
    for observation, action in pairs:
        counts[observation][action] += 1
    return {state: sorted(hist.items(),
                         key=lambda p: (-p[1], p[0]))[0][0]
            for state, hist in counts.items()}


def rollout(policy, scenario):
    visited = []
    states = (["start", "recovery", "known"]
              if scenario == "conflict"
              else ["start", "missing", "known"]
              if scenario == "missing"
              else ["start", "known"])
    for state in states:
        visited.append(state)
        if policy.get(state, "draft") != EXPERT[state]:
            return False, visited
    return True, visited


def evaluate(policy, tasks):
    return sum(rollout(policy, task)[0] for task in tasks)


def run():
    tasks = ["normal", "missing", "conflict"] * 10
    baseline = fit(INITIAL)
    pairs = list(INITIAL)
    for scenario in tasks:
        _, visited = rollout(baseline, scenario)
        pairs.extend((state, EXPERT[state]) for state in visited)
    aggregated = fit(pairs)
    report = {"episodes": len(tasks),
              "baseline_success": evaluate(baseline, tasks),
              "aggregated_success": evaluate(aggregated, tasks),
              "baseline_states": len(baseline),
              "aggregated_states": len(aggregated)}
    assert report["baseline_success"] == 20
    assert report["aggregated_success"] == 30
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
