'Конечная инструментальная среда без обучения языковой модели.'
from random import Random
import json

ACTIONS = ("read", "draft", "stop")


def transition(state, action, unsafe_reward=False):
    if action == "read":
        reward = 0.30 if unsafe_reward else -0.05
        return 1, reward, False, False
    if action == "draft":
        accepted = state == 1
        return 2, 1.0 if accepted else -0.5, True, accepted
    return 2, 0.0, True, False


def best(q, state):
    return max(range(3), key=lambda a: (q[state][a], -a))


def train(seed, unsafe_reward=False, episodes=3000):
    rng = Random(seed)
    q = [[0.0] * 3 for _ in range(2)]
    for _ in range(episodes):
        state = 0
        for step in range(20):
            action = (rng.randrange(3) if rng.random() < 0.15
                      else best(q, state))
            next_state, reward, done, _ = transition(
                state, ACTIONS[action], unsafe_reward)
            target = reward
            if not done:
                target += 0.95 * max(q[next_state])
            q[state][action] += 0.1 * (target - q[state][action])
            if done:
                break
            state = next_state
        # Горизонт ограничивает наблюдение и не завершает состояние среды.
    return q


def evaluate(q, episodes=20):
    accepted = 0
    truncated = 0
    calls = 0
    for _ in range(episodes):
        state = 0
        for step in range(20):
            action = best(q, state)
            state, _, done, success = transition(
                state, ACTIONS[action])
            calls += 1
            if done:
                accepted += int(success)
                break
        else:
            truncated += 1
    return {"accepted": accepted, "truncated": truncated,
            "calls": calls, "episodes": episodes}


def run():
    reports = []
    for seed in (11, 23, 47):
        good = train(seed)
        bad = train(seed, unsafe_reward=True)
        good_report = evaluate(good)
        bad_report = evaluate(bad)
        assert good_report["accepted"] == 20
        assert good_report["calls"] == 40
        assert bad_report["accepted"] == 0
        assert bad_report["truncated"] == 20
        reports.append({"seed": seed,
                        "goal_reward": good_report,
                        "read_bonus": bad_report})
    return reports


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
