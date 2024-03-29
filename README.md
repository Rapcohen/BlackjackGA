# Genetic Algorithm Solution for Blackjack


## Introduction

The goal of this project is to find the optimal [Blackjack](https://en.wikipedia.org/wiki/Blackjack) strategy by using a
genetic algorithm.

Blackjack is a popular card game that is played in casinos all over the world. It is also known as 21, as the goal of 
the game is to get a hand value of 21 or as close to 21 as possible without going over.

In blackjack, each player is dealt two cards and then has the option to "hit" and receive additional cards or "stand" 
and keep their current total. The dealer also hits or stands according to a set of rules that are determined by the 
casino. The player's hand is compared to the dealer's hand, and the player wins if their hand has a higher value than 
the dealer's hand or if the dealer goes over 21.

Blackjack can be played with one or more decks of cards, and the value of the cards is as follows: all face cards 
(kings, queens, and jacks) are worth 10, aces are worth 1 or 11 (player's choice), and all other cards are worth their 
face value.

There are many variations of blackjack, and the specific rules can vary from one casino to another. However, the basic 
principles of the game are the same everywhere.


## What is a Blackjack Strategy?

A Blackjack strategy is basically a lookup table which tells the player which action to take according to the current
state of the game.

The state of the game is defined by the player's hand and the dealer's up card.

There are two types of Blackjack hands: **hard** and **soft**:

- If a hand contains an ace which can be counted as 11 without busting, then it is a soft hand.
- Otherwise, it is a hard hand.

A strategy is usually represented by two tables, one for hard hands and the other for soft hands.

The optimal Blackjack strategy was already found by [Edward O. Thorp](https://en.wikipedia.org/wiki/Edward_O._Thorp) in
the 1960s:

![Optimal Strategy for Blackjack](images/classic_optimal_strategy.png)

In this strategy, 'H' means **hit**, 'S' means **stand**, and 'D' means **double down**. There is also a third table with
'P's in it - which means **split**, meaning that his strategy is for a form of Blackjack that allows split.
For simplicity, in this project we will try to find the optimal strategy for Blackjack games in which split is not allowed.

The fact that an optimal strategy has already been found will allow us to compare the results of our algorithm with the best known
solution and know how well we did.

## Why Use a Genetic Algorithm?

A genetic algorithm is a search algorithm that is inspired by the process of natural selection.

It works by creating a population of random solutions, then repeatedly creating a new generation of solutions by
combining the best solutions of the previous generation.
Some solutions are mutated in order to introduce diversity in the population.
The process is repeated until a solution is found that meets the desired criteria or the maximum number of generations
is reached.

A genetic algorithm is especially useful when the search space is very large, and it is not possible to search it
exhaustively in a reasonable amount of time.

This is exactly the case of the Blackjack strategy problem, as there is a huge number of possible strategies:

- The hard hands table has 170 entries.
- The soft hands table has 80 entries.
- There are 3 possible actions for each entry (in our simplified version without the split action).
- In total there are 3^250 possible strategies.

## Algorithm Settings

### Representation

We need to a way to represent the individuals of the population.
In our case, the individuals are Blackjack strategies.

As we have written above, a strategy is usually represented by two tables, one for hard hands and one for soft hands.

This is exactly how we are going to represent the strategies in our genetic algorithm:

- The hard hands table is represented by a 17x10 matrix.
- The soft hands table is represented by a 8x10 matrix.
- Each entry in these matrices holds an action (HIT / STAND / DOUBLE DOWN).

### Fitness Score

We need a way to evaluate the quality of a strategy.
The fitness score is a numeric value that represents how good a strategy is. The higher the score, the better the
strategy.

Basically, we are going to simulate a large number of rounds of Blackjack using the strategy, then count the number of
credits we have at the end.

In more detail, The fitness score is calculated as follows:

- Start with 0 credits.
- Simulate a large number of rounds of Blackjack against the dealer:
    - In the start of each round, place a fixed bet of 1 credit.
    - Play according to the given strategy.
- Return the final number of credits.

The only question left is, how many rounds should we simulate?

Since Blackjack is a game of chance, we need to play a large number of rounds in order to get a good estimate of the
strategy's quality.
This is especially critical for later generations, where strategies become very similar as they converge to the optimal
one.

After some experimentation, we found that simulating 500,000 rounds strikes a good balance between the time it takes to
calculate the fitness score and the accuracy of the fitness score.

### Selection

We need a way to select the best strategies from the population.
The strategies are compared using their fitness score.

There are several ways to select the best strategies from the population.
In this project, we are going to use the tournament selection method.

The tournament selection method selects a random subset of the population, then selects the best strategy from this
subset.
The number of strategies in each subset is called the tournament size.

We have decided to use tournament selection with a tournament size of 2.

The reason we went with this method is that it is fast, easy to understand and works well in most cases.
It also avoids pitfalls such as premature convergence which could occur when using methods like roulette wheel
selection.

### Elitism

We need a way to preserve the best strategies from the previous generation.
This can be achieved by using a technique called elitism.

It is a simple technique that copies the best strategies from the previous generation to the next generation without any
modifications.

We have decided to use a small elitism rate of 0.01 (1%).

This preserves the best strategies from the previous generation, while still allowing the population to evolve.

### Crossover

We need a way to combine strategies from the previous generation to create new strategies.
A crossover can be done in many elaborate ways, but in our case we are going to do something quite straightforward.
Given two strategies, we iterate over all entries in both tables, and swap the entries between the two strategies with a
probability of 0.5 (50%).

### Mutation

We need a way to mutate the strategies in order to introduce diversity in the population.

This is quite simple in our case, as we can simply change the action of a random entries in the tables.

Another thing to consider is the mutation rate, which is the probability that a mutation will occur in a new strategy.
We are using a small mutation rate of 0.05 (5%).

### Population Size

The size of the population is the number of strategies in each generation.
It has a big impact on both the speed and the quality of the algorithm.

A large population size is important for finding the optimal solution since it allows the algorithm to explore a large
part of the search space.
However, a large population size also means that the algorithm will take longer to run.

We have experimented with population sizes ranging from 100 to 1000, and we have found that a population size of 1000
gives satisfactory results.

## Results

Before showing the results, we need to address an issue about the fitness scores.

When simulating a large enough number of rounds, the fitness score of any strategy will almost certainly be negative.
Therefore, when looking at the results, we should see the improvement over the generations when the fitness scores
approach zero.

Why does this happen?

- Ever heard the saying "the house always wins"?
- The typical hand of Blackjack gives you a 42.22% chance of winning, while the tie stands at around 8.48% (which means
  that you lose ~50% of the time).
- This means that any player, no matter the strategy, will lose money in the long run.
- When calculating the fitness, we are simulating a huge number of rounds, which eventually leads to a loss, resulting
  in a negative fitness score.

Running the algorithm with the settings described above for 70 generations yields the following results:

| Generation | Best Fitness Score | Worst Fitness Score | Average Fitness Score |
|------------|--------------------|---------------------|-----------------------|
| #1         | -165306            | -295196             | -233271               |
| #10        | -98041             | -185088             | -139774               |
| #20        | -65134             | -111275             | -86320                |
| #30        | -48831             | -102021             | -60355                |
| #40        | -40675             | -55615              | -46776                |
| #50        | -34777             | -53917              | -40360                |
| #60        | -32267             | -43943              | -37113                |
| #70        | -30973             | -44163              | -35399                |

![Evolution](images/evolution.gif)

| Known Optimal Strategy                           | Our Best Strategy                   |
|--------------------------------------------------|-------------------------------------|
| ![Optimal Strategy](images/optimal_strategy.png) | ![Best Strategy](images/gen-70.png) |

Overall, the algorithm was able to come close to the optimal strategy in 70 generations.

In fact, we simulated 500,000 hands using the known optimal strategy and got a fitness score of -33342, while the best fitness
score in the 70th generation is -30973, which means that in our simulation we even did a better job than the optimal strategy.

Since Blackjack is not a deterministic game, we can't know for sure whether one strategy is better than the other or not,
but nevertheless getting this close to the optimal strategy in 70 generations is quite impressive.

[//]: # (## Conclusion)

[//]: # (TODO)

## Notes

1. 3rd party libraries used:
    - [EC-Kity (Version 0.2.3)](https://pypi.org/project/eckity/) for the genetic algorithm execution.
    - [blackjack21 (version 1.2.1)](https://pypi.org/project/blackjack21/) for the Blackjack simulation
2. Performance:
    - The algorithm takes a long time to run with the settings mentioned above.
    - The bottleneck is the fitness score calculation, which simulates many rounds of Blackjack per strategy.
    - The results shown here were obtained after running the algorithm for over 48 hours, and after altering the EC-Kity
      library in our local virtual environment so that it'll use ProcessPoolExecutor instead of ThreadPoolExecutor.
      The local changes can be found [here](https://github.com/EC-KitY/EC-KitY/compare/main...Rapcohen:EC-KitY:process-pool-executor)

## Usage

1. Install the required libraries: `pip install -r requirements.txt`
2. Run the algorithm: `python main.py`
3. The results will be saved in the `results` folder (the best strategy in each generation will be saved as a CSV file).

## Authors

Raphael Cohen & Keren Tzidki