import csv
import time
from copy import deepcopy
from datetime import datetime

from ga import algo, StrategyIndividual


def save_to_csv(best_individual: StrategyIndividual):
    with open(f"results\\{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hard Hands:"])
        writer.writerow(["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"])
        i = 20
        hard = deepcopy(best_individual.strategy.hard_hands)
        hard.reverse()
        for row in hard:
            writer.writerow([i, *[str(item) for item in row]])
            i -= 1
        writer.writerow(["Soft Hands:"])
        writer.writerow(["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"])
        i = 9
        soft = deepcopy(best_individual.strategy.soft_hands)
        soft.reverse()
        for row in soft:
            writer.writerow([f"A-{i}", *[str(item) for item in row]])
            i -= 1


if __name__ == "__main__":
    start_time = time.time()
    algo.evolve()
    print("--- %.2f seconds ---" % (time.time() - start_time))
    save_to_csv(algo.best_of_run_)
