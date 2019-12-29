import random


class TSP:
    # n cities, euclidien coordinates x, y
    def __init__(self, coordinates, distances):
        self.coordinates = coordinates  # list of tuples of each node's x, y coordinate
        self.distances = distances  # matrix n x n of distance.


    def optimize(self, method, args):
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


    def random_representation(self):
        """ create random_representation """
        sample = [i for i in range(len(self.coordinates))]
        random.shuffle(sample)
        sample.append(sample[0])  # end at where you began
        return sample


    def fitness(self, representation):
        """ smaller the fitness, the better it is """
        # representation: length n int array of city sequence
        total = 0
        prev_city = -1  # no city number -1
        for city in representation:
            if prev_city == -1:
                prev_city = city
                continue
            total += self.distances[prev_city][city]
            prev_city = city
        return total


    def make_solution_file(self, representation):
        # create, and put the sequence of nodes in solution.csv file
        s = "\n".join([str(i+1) for i in representation])
        with open("solution.csv", "w") as file:
            file.write(s)

    def exit_on_fitness_limit(self, best, best_fitness):
        print("exiting due to fitness limit..\n"
              "Current best is: ", best_fitness)
        self.make_solution_file(best)
        exit(0)

