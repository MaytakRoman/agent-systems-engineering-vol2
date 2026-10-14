from learning import fit, rollout, evaluate, INITIAL, EXPERT

policy = fit(INITIAL)
assert not rollout(policy, "conflict")[0]
assert "recovery" not in policy
augmented = fit(INITIAL + [("recovery", EXPERT["recovery"])])
for order in (["normal", "missing", "conflict"],
              ["conflict", "normal", "missing"]):
    assert evaluate(policy, order) == 2
    assert evaluate(augmented, order) == 3
negative = fit(INITIAL * 20)
assert not rollout(negative, "conflict")[0]
print('Покрытие, порядок и отрицательный контроль проверены')
