import csv
import os


def save_result_to_csv_file(execution_date_time, best_individual, generation):
    directory_path = os.path.join("results", execution_date_time.strftime("%Y-%m-%d_%H-%M-%S"))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file_path = os.path.join(directory_path, f"gen-{generation}.csv")
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"])
        for i, row in zip(range(20, 3, -1), reversed(best_individual.strategy.hard_hands)):
            writer.writerow([i, *[str(action) for action in row]])
        writer.writerow([])
        writer.writerow(["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"])
        for i, row in zip(range(9, 1, -1), reversed(best_individual.strategy.soft_hands)):
            writer.writerow([f"A-{i}", *[str(action) for action in row]])
        writer.writerow([])
        writer.writerow([""] * 4 + ["Fitness", best_individual.get_pure_fitness()] + [""] * 4)
