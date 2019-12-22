import math
import random

# TODO: export TSP
class TSP:
    # n cities, euclidien coordinates x, y
    def __init__(self):
        self.coordinates = []  # list of tuples of each node's x, y coordinate
        self.distances = []  # matrix n x n of distance.


def run():
    """ entry point to our implementation """
    # Representation: [] -> the number in order of visited nodes
    # Fitness Function: int -> the sum of root of all traveled values above.
    # Operators: Random

    # starting representations
    start, start_fitness = make_unbiased_initial()
    # random restart, 2nd group for local search
    restart, restart_fitness = make_unbiased_initial()

    # == local optima == #
    print("Local Search..")
    local1, local_fitness1, loops1 = local_search(start, start_fitness)
    best_fitness1 = local_fitness1[population_size-1]
    make_solution_file(local1[population_size-1])  # in case of ending after Local Search 1
    print("Local Search 1: ", best_fitness1)
    local2, local_fitness2, loops2 = local_search(restart, restart_fitness, loops1)
    best_fitness2 = local_fitness2[population_size-1]
    print("Local Search 2: ", best_fitness2)
    optima = local1 + local2

    # best after two Local Search
    if best_fitness1 > best_fitness2:
        best = local2[population_size-1]
    else:
        best = local1[population_size-1]

    # == Genetic Algorithm == #
    # with fine dataset of neighbour size representation, do genetic.
    print("Genetic Algorithm..")
    best, best_fitness = genetic_algorithm(optima, best, loops2)

    # # == Pure Random == #
    # # act as a "base case", standard
    # best, best_fitness = make_unbiased_initial()

    # export 'best' to solution file
    print("distance traveled: ", best_fitness)
    make_solution_file(best)


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


def local_search(start, start_fitness, loops=0):
    """ local search, and best results """
    # switch two road paths.. / 2-opt
    bests = []
    best_fitnesses = []
    while 1:
        N = get_neighbours(start)
        for n in N:
            new_fitness = fitness(n)
            if new_fitness < start_fitness:
                start = n
                start_fitness = new_fitness
                # print(start_fitness)
        # keep track of recent
        bests.append(start)
        best_fitnesses.append(start_fitness)
        # check fitness limit
        loops += 1
        if loops > fitness_limit:
            exit_on_fitness_limit(bests[len(bests)-1], best_fitnesses[len(best_fitnesses)-1])
        if break_condition(bests, best_fitnesses, loops):
            break
    return bests, best_fitnesses, loops


def exit_on_fitness_limit(best, best_fitness):
    print("exiting due to fitness limit..\n"
          "Current best is: ", best_fitness)
    make_solution_file(best)
    exit(0)


def break_condition(recent_bests, recent_best_fitnesses, loops):
    """ breaks when near local optima """
    if len(recent_bests) < population_size+1:  # size of bests are neighbour_size
        return False
    recent_bests.pop(0)
    recent_best_fitnesses.pop(0)
    l = len(recent_best_fitnesses)
    improvements = (recent_best_fitnesses[0] - recent_best_fitnesses[l-1]) / recent_best_fitnesses[0]
    # # messages..
    # if loops % 500 == 0:
    #     print("'Hang on..' Still improving at: %.4f%%" % (improvements*100))
    # if recent improvement goes below 0.05%, break
    if improvements < 0.0005:
        return True


def make_unbiased_initial():
    """ initial sampling, excluding extremes """
    start = random_representation()
    start_fitness = fitness(start)
    # Random: To prevent extreme initial cases.
    for _ in range(100):  # TODO: how many should be enough?
        new = random_representation()
        new_fitness = fitness(new)
        if new_fitness < start_fitness:
            start = new
            start_fitness = new_fitness
    return start, start_fitness


def get_neighbours(representation):
    """ neighbours created with swapping two roads, 2-opt """
    l = len(representation)
    neighbours = []
    for _ in range(neighbour_size):  # slow loop for large sizes, lack of exploitation for small sizes.
        a, b = [random.choice(range(0, l-1)) for _ in range(2)]  # exclude last elem which is repeated
        high = max(a, b)
        low = min(a, b)
        if high-low <= 1:
            continue
        new = representation[:low] + representation[low:high][::-1] + representation[high:]
        if low == 0:  # must equalize endpoint
            new[l-1] = new[0]
        neighbours.append(new)
    return neighbours


def random_representation():
    """ create random_representation """
    sample = [i for i in range(len(tsp.coordinates))]
    random.shuffle(sample)
    sample.append(sample[0])  # end at where you began
    return sample


def fitness(representation):
    """ smaller the fitness, the better it is """
    # representation: length n int array of city sequence
    total = 0
    prev_city = -1  # no city number -1
    for city in representation:
        if prev_city == -1:
            prev_city = city
            continue
        total += tsp.distances[prev_city][city]
        prev_city = city
    return total


def make_solution_file(representation):
    # create, and put the sequence of nodes in solution.csv file
    s = "\n".join([str(i+1) for i in representation])
    with open("solution.csv", "w") as file:
        file.write(s)

