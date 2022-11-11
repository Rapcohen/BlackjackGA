import random

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.creators.creator import Creator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness.fitness import Fitness
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.individual import Individual
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from blackjack import Strategy, simulate_hands, Action


class StrategyIndividual(Individual):
    def __init__(self, strategy: Strategy, fitness: Fitness):
        super().__init__(fitness)
        self.strategy = strategy

    def show(self):
        pass


class StrategyEvaluator(SimpleIndividualEvaluator):
    def __init__(self, n_hands: int):
        super().__init__()
        self.n_hands = n_hands

    def _evaluate_individual(self, individual: StrategyIndividual):
        return simulate_hands(n_hands=self.n_hands, strategy=individual.strategy)


class StrategyCreator(Creator):
    def create_individuals(self, n_individuals, higher_is_better):
        return [StrategyIndividual(self.random_strategy(), SimpleFitness(higher_is_better=higher_is_better)) for _ in
                range(n_individuals)]

    def random_strategy(self):
        hard_hands = [[self.random_action() for _ in range(Strategy.hard_hands_dim[1])] for _ in
                      range(Strategy.hard_hands_dim[0])]
        soft_hands = [[self.random_action() for _ in range(Strategy.soft_hands_dim[1])] for _ in
                      range(Strategy.soft_hands_dim[0])]
        return Strategy(hard_hands=hard_hands, soft_hands=soft_hands)

    @staticmethod
    def random_action():
        return random.choice(list(Action))


class StrategyCrossover(GeneticOperator):
    def __init__(self, probability=1, arity=2, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        for i in range(Strategy.hard_hands_dim[0]):
            for j in range(Strategy.hard_hands_dim[1]):
                if random.random() < 0.5:
                    self.swap_hard(individuals, i, j)

        for i in range(Strategy.soft_hands_dim[0]):
            for j in range(Strategy.soft_hands_dim[1]):
                if random.random() < 0.5:
                    self.swap_soft(individuals, i, j)

        self.applied_individuals = individuals
        return individuals

    @staticmethod
    def swap_hard(individuals, i, j):
        individuals[0].strategy.hard_hands[i][j], individuals[1].strategy.hard_hands[i][j] = \
            individuals[1].strategy.hard_hands[i][j], individuals[0].strategy.hard_hands[i][j]

    @staticmethod
    def swap_soft(individuals, i, j):
        individuals[0].strategy.soft_hands[i][j], individuals[1].strategy.soft_hands[i][j] = \
            individuals[1].strategy.soft_hands[i][j], individuals[0].strategy.soft_hands[i][j]


class StrategyMutation(GeneticOperator):
    def __init__(self, probability=1, arity=1, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        if random.random() < 0.01:
            i = random.randint(0, Strategy.hard_hands_dim[0] - 1)
            j = random.randint(0, Strategy.hard_hands_dim[1] - 1)
            individuals[0].strategy.hard_hands[i][j] = random.choice(list(Action))
        if random.random() < 0.01:
            i = random.randint(0, Strategy.soft_hands_dim[0] - 1)
            j = random.randint(0, Strategy.soft_hands_dim[1] - 1)
            individuals[0].strategy.soft_hands[i][j] = random.choice(list(Action))

        self.applied_individuals = individuals
        return individuals


algo = SimpleEvolution(
    population=Subpopulation(
        evaluator=StrategyEvaluator(n_hands=100000),
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
        population_size=8,  # find optimal value
        individuals=None,
        higher_is_better=True
    ),
    max_generation=60,  # find optimal value
    max_workers=None,  # uses all available cores
    statistics=BestAverageWorstStatistics(),
)
