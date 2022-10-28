# Representation

- two tables (matrices): HARD-HANDS and SOFT-HANDS
- each column represents a dealer's card
- each row represents a player's hand
- each cell represents the action to take (HIT, STAND, DOUBLE)
- HARD-HANDS (16 x 10): row values are 4 - 20
- SOFT-HANDS (8 x 10): row values are ACE+2 - ACE+9

# Fitness

- number of chips left after N hands
- will be normalized to non-negative values

# Selection:

- TBD (tournament, roulette, etc.)

# Elitism:

- will be applied to the best X% of the population

# Crossover:

- Relative to the fitness of the parents

# Mutation:

- TBD (rate, impact)

# Population:

- TBD (size, N-generations)