import argparse
import os
import math
from tsp import *


def main():
    # Get dataset, Parse parameters
    parser = argparse.ArgumentParser(
        description="Implement various heuristic methods to solve TSP\r\n\r\n"
        "(Default) Genetic Algorithm, rl11849.tsp"
    )

    # (Default) python tsp_solver.py --method GA --instance data/rl11849.tsp --population_size 200
    parser.add_argument(
        "--method",
        "-m",
        default="GA",
        help="which heuristic method to solve TSP:\n Greedy, 2-Opt, GA, ACO, PSO",
    )
    parser.add_argument(
        "--file",
        "-f",
        default="data/rl11849.tsp",
        help="TSP file instance name to solve (in data folder) (ex) data/a280.tsp",
    )
    # 2-opt Algorithm
    parser.add_argument(
        "--neighbour_size",
        "-n",
        type=int,
        default=50,
        help="get_neighbours() size for local search",
    )
    # Genetic Algorithm
    parser.add_argument(
        "--population_size", "-p", type=int, default=200, help="population size for GA"
    )
    parser.add_argument(
        "--fitness_limit",
        "-limit",
        type=float,
        default=math.inf,
        help="fitness function limits",
    )

    # Modes, Params
    args = parser.parse_args()
    if args.method == "Greedy":
        method = "Greedy Search"
        parameters = ""
    elif args.method == "2-Opt":
        method = "2-Optimization"
        parameters = "neighbour size: %d" % (args.neighbour_size)
    elif args.method == "GA":
        method = "Genetic Algorithm"
        parameters = "population: %d, fitness limit: %f" % (
            args.population_size,
            args.fitness_limit,
        )
    elif args.method == "ACO":
        method = "Ant Colony Optimization"
        parameters = ""
    elif args.method == "PCO":
        method = "Particle Swarm Optimization"
        parameters = ""
    else:
        print("Please check you method: one of .. Greedy, 2-Opt, GA, ACO, PSO")
        exit(0)

    # Running with..
    print("Running solver with.. {}, {}".format(method, os.path.split(args.file)[1]))
    if parameters != "":  # params
        print("Parameters: " + parameters)

    # Execute Optimization
    coordinates, distances = parse_data(args.file)
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
            if line != "EOF" and start:
                line = line.strip()
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
