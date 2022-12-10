import random
import statistics

from blackjack import Strategy, Action, simulate_hands


def random_strategy():
    hard_hands = [[random_action() for _ in range(Strategy.hard_hands_dim[1])] for _ in
                  range(Strategy.hard_hands_dim[0])]
    soft_hands = [[random_action() for _ in range(Strategy.soft_hands_dim[1])] for _ in
                  range(Strategy.soft_hands_dim[0])]
    return Strategy(hard_hands=hard_hands, soft_hands=soft_hands)


def random_action():
    return random.choice(list(Action))


def optimal_strategy() -> Strategy:
    return Strategy(
        hard_hands=[
            [Action.HIT] * 10,
            [Action.HIT] * 10,
            [Action.HIT] * 10,
            [Action.HIT] * 10,
            [Action.HIT] * 10,
            [Action.HIT] + [Action.DOUBLE_DOWN] * 4 + [Action.HIT] * 5,
            [Action.DOUBLE_DOWN] * 8 + [Action.HIT] * 2,
            [Action.DOUBLE_DOWN] * 10,
            [Action.HIT] * 2 + [Action.STAND] * 3 + [Action.HIT] * 5,
            [Action.STAND] * 5 + [Action.HIT] * 5,
            [Action.STAND] * 5 + [Action.HIT] * 5,
            [Action.STAND] * 5 + [Action.HIT] * 5,
            [Action.STAND] * 5 + [Action.HIT] * 5,
            [Action.STAND] * 10,
            [Action.STAND] * 10,
            [Action.STAND] * 10,
            [Action.STAND] * 10,
        ],
        soft_hands=[
            [Action.HIT] * 3 + [Action.DOUBLE_DOWN] * 2 + [Action.HIT] * 5,
            [Action.HIT] * 3 + [Action.DOUBLE_DOWN] * 2 + [Action.HIT] * 5,
            [Action.HIT] * 2 + [Action.DOUBLE_DOWN] * 3 + [Action.HIT] * 5,
            [Action.HIT] * 2 + [Action.DOUBLE_DOWN] * 3 + [Action.HIT] * 5,
            [Action.HIT] + [Action.DOUBLE_DOWN] * 4 + [Action.HIT] * 5,
            [Action.DOUBLE_DOWN] * 5 + [Action.STAND] * 2 + [Action.HIT] * 3,
            [Action.STAND] * 4 + [Action.DOUBLE_DOWN] + [Action.STAND] * 5,
            [Action.STAND] * 10,
        ],
    )


if __name__ == '__main__':
    user_input = input("Use optimal strategy? (y/n): ")
    n_hands = int(input("Number of hands to simulate: "))
    strategy = optimal_strategy() if user_input == 'y' else random_strategy()
    results = [simulate_hands(n_hands, strategy) for _ in range(50)]
    mean = statistics.mean(results)
    distance = abs(max(results) - min(results))
    print(f"results: {results}")
    print(f"min: {min(results)}")
    print(f"max: {max(results)}")
    print("mean: %.2f" % mean)
    print(f"|max - min|: {distance}")
    print("|max - min| / n: %.5f" % (distance / n_hands))
