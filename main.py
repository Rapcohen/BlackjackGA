from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.creators.creator import Creator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.subpopulation import Subpopulation


class StrategyEvaluator(SimpleIndividualEvaluator):
    def _evaluate_individual(self, individual):
        # simulate N hands using this strategy and return the normalized chip count (non-negative)
        pass


class StrategyCreator(Creator):
    def create_individuals(self, n_individuals, higher_is_better):
        # create n individuals with random strategies
        pass


class StrategyCrossover(GeneticOperator):
    def apply(self, individuals):
        # apply crossover to the individuals (relative to their fitness)
        pass


class StrategyMutation(GeneticOperator):
    def apply(self, individuals):
        # apply mutation to the individuals
        pass


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
    max_generation=100  # find optimal value
)

algo.evolve()
algo.finish()
