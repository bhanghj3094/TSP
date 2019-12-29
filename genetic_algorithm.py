import math
import random

def genetic_algorithm(optima, best, loops):
    """ leave all under 103% * current best_fitness, leave part(10%) for over 103% """
    best_fitness = fitness(best)
    # include diversity
    for _ in range(int(0.2 * population_size)):
        optima.append(random_representation())
    # create next generation equal to parent population size
    first_generation = [create_child(optima) for _ in range(population_size)]
    best, best_fitness = get_best(first_generation, best, best_fitness)
    for _ in range(500):
        # select parents
        pooling = []
        for child in first_generation:
            if fitness(child) < best_fitness * 1.03:
                pooling.append(child)
            elif random.random() < 0.1:
                pooling.append(child)
        # next of next_generation
        next_generation = [create_child(pooling) for _ in range(population_size)]
        best, best_fitness = get_best(next_generation, best, best_fitness)
        # check fitness limit
        loops += 1
        if loops > fitness_limit:
            exit_on_fitness_limit(best, best_fitness)
    return best, best_fitness


def get_best(representations, best, best_fitness):
    for elem in representations:
        elem_fitness = fitness(elem)
        if elem_fitness < best_fitness:
            best = elem
            best_fitness = elem_fitness
    return best, best_fitness


def create_child(parent_group):
    """ crossover for parents in the group """
    parent1 = random.choice(parent_group)
    parent2 = random.choice(parent_group)
    # slice gene from parent1
    i, j = [random.choice(range(0, len(parent1) - 1)) for _ in range(2)]
    # create child
    child1 = parent1[min(i, j): max(i, j)+1]
    child2 = [gene for gene in parent2 if gene not in child1]
    return child1 + child2 + [child1[0]]