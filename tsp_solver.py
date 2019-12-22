import sys  # not used yet
import argparse
from pprint import pprint  # not used yet
from timeit import timeit  # not used yet
from two_opt import *

# Also move functions in to TSP instances. 

def main():
    global tsp

    # Get dataset, Parse parameters
    parser = argparse.ArgumentParser(description="Implement various heuristic methods to solve TSP\n\n (Default) Genetic Algorithm, rl11849.tsp")

    # (Default) python tsp_solver.py --method GA --instance data/rl11849.tsp --population_size 200
    parser.add_argument("--method", "-m", default="GA", help="which heuristic method to solve TSP:\n Greedy, 2-opt, GA, ACO, PSO")
    parser.add_argument("--file", "-f", default="data/rl11849.tsp", help="TSP file instance to solve (in data folder) (ex) data/a280.tsp")
    # 2-opt Algorithm
    parser.add_argument("--neighbour_size", "-n", type=int, default=50, help="get_neighbours() size for local search")
    # Genetic Algorithm
    parser.add_argument("--population_size", "-p", type=int, default=200, help="population size for GA")
    parser.add_argument("--fitness_limit", "-limit", default=math.inf, help="fitness function limits")

    # Running with..
    args = parser.parse_args()
    print("Running solver with.. {}, {}".format(args.method, args.file))
    if args.method == "Greedy":
        pass
    elif args.method == "2-opt":
        print("[Args] neighbour size: %s" % (args.neighbour_size))
    elif args.method == "GA":
        print("[Args] population: %d, fitness limit: %f" % (args.population_size, args.fitness_limit))
    elif args.method == "ACO":
        pass
    elif args.method == "PCO":
        pass
    else:
        pass

    # initialize tsp instance
    tsp = TSP()

    # parse file..
    if not check_file_format(args.file):
        print("[Invalid data] \n"
              "Please check the instance file format from: \n\n"
              "    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html\n")
        exit(0)
    fitness_limit = float(args.fitness_limit)
    neighbour_size, population_size = args.neighbour_size, args.population_size
    run()

# if correct, return True / else return False
def check_file_format(file):
    global tsp
    try:
        # parse .tsp file, into TSP coordinates
        f = open(file, encoding='utf-8')
        line = f.readline()
        while line != "NODE_COORD_SECTION\n":
            line = f.readline()
        for line in f:
            line = line.strip()
            if line == "EOF":
                break
            coordinate = line.split(" ")
            coordinate = [i for i in coordinate if i != '']
            tsp.coordinates.append((float(coordinate[1]), float(coordinate[2])))
        f.close()
        # TSP coordinates to TSP distances matrix
        c = tsp.coordinates
        cl = len(c)
        print("Making TSP node distances matrix..")
        tsp.distances = [
            [math.hypot(c[i][0] - c[j][0], c[i][1] - c[j][1]) for j in range(cl)] for i in range(cl)
        ]  # [math.sqrt((c[i][0] - c[j][0]) ** 2 + (c[i][1] - c[j][1]) ** 2) for j in range(cl)] for i in range(cl)
        return True
    except ValueError:  # other Errors..?
        return False

# Runs on >> python tsp_solver.py
# Do not run on >> import tsp_solver
if __name__ == '__main__':
    main()
