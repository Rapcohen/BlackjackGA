import random

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


class StrategyEvaluator(SimpleIndividualEvaluator):
    def _evaluate_individual(self, individual: StrategyIndividual):
        # simulate N hands using this strategy and return the normalized chip count (non-negative)
        return simulate_hands(1000, individual.strategy)


class StrategyCreator(Creator):
    def random_action(self):
        return random.choice(list(Action))

    def create_individuals(self, n_individuals, higher_is_better):
        # create n individuals with random strategies
        ivdividuals = []
        for _ in range(n_individuals):
            strategy = Strategy(
                [[self.random_action() for _ in range(17)] for _ in range(10)],
                [[self.random_action() for _ in range(8)] for _ in range(10)],
            )
            ivdividuals.append(StrategyIndividual(strategy, SimpleFitness(higher_is_better=higher_is_better)))
        return ivdividuals


class StrategyCrossover(GeneticOperator):
    def apply(self, individuals):
        # apply crossover to the individuals (relative to their fitness)
        return individuals


class StrategyMutation(GeneticOperator):
    def apply(self, individuals):
        # apply mutation to the individuals
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
            TournamentSelection(tournament_size=2, higher_is_better=True, events=None)
        ],
        elitism_rate=0.01,  # find optimal value
        population_size=100,  # find optimal value
        individuals=None,
        higher_is_better=True
    ),
    statistics=None,
    max_generation=10  # find optimal value
)

if __name__ == "__main__":
    algo.evolve()
    algo.finish()
