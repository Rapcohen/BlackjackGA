import random
from copy import deepcopy

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.creators.creator import Creator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness.fitness import Fitness
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.individual import Individual
from eckity.subpopulation import Subpopulation

from blackjack import Strategy, simulate_hands, Action


class StrategyIndividual(Individual):
    def __init__(self, strategy: Strategy, fitness: Fitness):
        super().__init__(fitness)
        self.strategy = strategy

    def show(self):
        hard = deepcopy(self.strategy.hard_hands)
        hard.reverse()
        soft = deepcopy(self.strategy.soft_hands)
        soft.reverse()
        print("Hard Hands:")
        print(f"\t {['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']}")
        i = 20
        for row in hard:
            print(f'{i}\t {[str(item) for item in row]}')
            i -= 1
        print("Soft Hands:")
        for row in soft:
            print([str(item) for item in row])


class StrategyEvaluator(SimpleIndividualEvaluator):
    def _evaluate_individual(self, individual: StrategyIndividual):
        # simulate N hands using this strategy and return the normalized chip count (non-negative)
        return simulate_hands(100000, individual.strategy)


class StrategyCreator(Creator):
    def random_action(self):
        return random.choice(list(Action))

    def create_individuals(self, n_individuals, higher_is_better):
        # create n individuals with random strategies
        ivdividuals = []
        for _ in range(n_individuals):
            strategy = Strategy(
                [[self.random_action() for _ in range(10)] for _ in range(17)],
                [[self.random_action() for _ in range(10)] for _ in range(8)],
            )
            ivdividuals.append(StrategyIndividual(strategy, SimpleFitness(higher_is_better=higher_is_better)))
        return ivdividuals


class StrategyCrossover(GeneticOperator):
    def __init__(self, probability=1, arity=2, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        for i in range(17):
            for j in range(10):
                if random.random() < 0.5:
                    self.swap_hard(individuals, i, j)

        for i in range(8):
            for j in range(10):
                if random.random() < 0.5:
                    self.swap_soft(individuals, i, j)

        self.applied_individuals = individuals
        return individuals

    def swap_hard(self, individuals, i, j):
        individuals[0].strategy.hard_hands[i][j], individuals[1].strategy.hard_hands[i][j] = \
            individuals[1].strategy.hard_hands[i][j], individuals[0].strategy.hard_hands[i][j]

    def swap_soft(self, individuals, i, j):
        individuals[0].strategy.soft_hands[i][j], individuals[1].strategy.soft_hands[i][j] = \
            individuals[1].strategy.soft_hands[i][j], individuals[0].strategy.soft_hands[i][j]


class StrategyMutation(GeneticOperator):
    def __init__(self, probability=1, arity=1, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        if random.random() < 0.01:
            i = random.randint(0, 16)
            j = random.randint(0, 9)
            individuals[0].strategy.hard_hands[i][j] = random.choice(list(Action))
        if random.random() < 0.01:
            i = random.randint(0, 7)
            j = random.randint(0, 9)
            individuals[0].strategy.soft_hands[i][j] = random.choice(list(Action))

        self.applied_individuals = individuals
        return individuals


algo = SimpleEvolution(
    population=Subpopulation(
        evaluator=StrategyEvaluator(),
        creators=StrategyCreator(),
        pcr=None,
        operators_sequence=[
            StrategyCrossover(),
            StrategyMutation(),
        ],
        selection_methods=[
            (TournamentSelection(tournament_size=2, higher_is_better=True, events=None), 1)
        ],
        elitism_rate=0.01,  # find optimal value
        population_size=100,  # find optimal value
        individuals=None,
        higher_is_better=True
    ),
    statistics=None,
    max_generation=20  # find optimal value
)

if __name__ == "__main__":
    algo.evolve()
    algo.finish()
