import argparse
import os
import math
from pprint import pprint
from tsp import *


def main():
    """
    Entry point for running genetic algorithms. 
    Implements various heuristic methods to solve 'Traveling Salesman Problem'.
    (Default)
        Method - Genetic Algorithm
        Dataset - a280.tsp
    Return. 
    """
    # Parameters
    parser = argparse.ArgumentParser()
    methods = "Greedy, 2-Opt, GA, ACO, PSO"
    parser.add_argument(
        "--method", default="GA", help="Heuristic methods: %s" % methods
    )
    parser.add_argument(
        "--file", default="a280", help="Dataset in data/ folder (ex) a280, bier127, .."
    )
    parser.add_argument(
        "--neighbour_size", type=int, default=50, help="Neighbour size used for 2-Opt",
    )
    parser.add_argument(
        "--population_size",
        type=int,
        default=200,
        help="Population size used for Genetic Algorithm",
    )
    parser.add_argument(
        "--fitness_limit",
        type=float,
        default=math.inf,
        help="Fitness evaluation limits used for Genetic Algorithm",
    )
    args = parser.parse_args()

    # Resolve Abbreviations
    white_space = "  "
    parameters = white_space + "None"
    if args.method == "Greedy":
        method = "Greedy Search"
    elif args.method == "2-Opt":
        method = "2-Optimization"
        parameters = white_space + "(Neighbour Size) %d" % (args.neighbour_size)
    elif args.method == "GA":
        method = "Genetic Algorithm"
        parameters = (
            white_space
            + "(Population Size) %d\n" % args.population_size
            + white_space
            + "(Fitness Evaluation Limit) %f" % args.fitness_limit
        )
    elif args.method == "ACO":
        method = "Ant Colony Optimization"
    elif args.method == "PCO":
        method = "Particle Swarm Optimization"
    else:
        print("Please check you method\nOne of .. %s" % methods)
        exit(0)

    # Running with..
    print(
        "Running solver..\n"
        + white_space
        + "(Method)  %s\n" % method
        + white_space
        + "(Dataset) %s" % os.path.split(args.file)[1]
    )
    print("Parameters..\n" + parameters)

    # Parse Data
    coordinates, distances = parse_data("data/" + args.file + ".tsp")

    # Run
    tsp = TSP(coordinates, distances)
    tsp.optimize(method, args)


# if correct, return True / else return False
def parse_data(file_path):
    coordinates = []
    try:
        f = open(file_path, "r")
        lines = f.readlines()
        start = False
        for line in lines:
            if line == "NODE_COORD_SECTION\n":  # starting point for coordinates
                start = True
                continue
            line = line.strip()
            if line != "EOF" and start:
                coordinate = line.split()
                coordinates.append((float(coordinate[1]), float(coordinate[2])))
        f.close()
        # Get TSP distances matrix
        cl = len(coordinates)
        print("Building TSP distances")
        distances = [
            [
                math.hypot(
                    coordinates[i][0] - coordinates[j][0],
                    coordinates[i][1] - coordinates[j][1],
                )
                for j in range(cl)
            ]
            for i in range(cl)
        ]
        return coordinates, distances
    except ValueError:
        print(
            "[Invalid data] \n"
            "Please check the instance file format from: \n\n"
            "    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html\n"
        )
        exit(0)


# Runs on >> python tsp_solver.py
# Do not run on >> import tsp_solver
if __name__ == "__main__":
    main()
