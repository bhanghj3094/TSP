

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

