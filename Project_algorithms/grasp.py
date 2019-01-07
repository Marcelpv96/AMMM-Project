import pickle
import math
from instance import Instance
from copy import deepcopy
from solution import Candidate, Solution
from restrictions import Restrictions
import random
from solver import Solver
from local_search import Local_search
import time


class Grasp(Solver):
    def __init__(self, instance, alpha=0.1, seed=96, k=10, seconds=60):
        self.instance = instance
        self.alpha = alpha
        self.k = k
        self.seconds = seconds
        random.seed(seed)

    def RCL(self, candidates_cost):
        q_max = candidates_cost[-1][1]
        q_min = candidates_cost[0][1]
        RCLmax = q_min + self.alpha*(q_max - q_min)
        nearest_value = min((cost[1] for cost in candidates_cost), key=lambda x:abs(x-RCLmax))
        RCL = [candidate[0] for candidate in filter(lambda y: y[1] <= nearest_value, candidates_cost)]
        return[candidate[0] for candidate in filter(lambda y: y[1] <= nearest_value, candidates_cost)]

    def selection_function(self, candidates, partial_solution):
        candidates_cost = [(candidate ,candidate.get_cost(partial_solution, self.instance)) for candidate in candidates]
        candidates_cost.sort(key=lambda x: x[1])
        candidates = [candidate[0] for candidate in candidates_cost]
        RCL = self.RCL(candidates_cost)
        return RCL[random.randint(0, len(RCL)-1)]

    def solve(self):
        best_sol = None
        best_cost = math.inf
        alpha = self.alpha
        iteration = 1
        start_time = time.time()
        while time.time() < start_time+self.seconds:
            self.alpha = 0 if iteration == 1 else alpha
            partial_solution = []
            candidates = self.get_candidates()
            while not self.solution_function(partial_solution):
                candidate = self.selection_function(candidates, partial_solution)
                if candidate:
                    partial_solution += [candidate]
                    candidates = self.update_candidates(candidates, partial_solution)
                    if not candidates:
                        break
                else:
                    break
            solution = Solution(partial_solution, self.instance)
            if solution.is_valid():
                ls = Local_search(solution)
                solution, cost = ls.run()
                if not solution:
                    best_sol = solution
                    best_cost = cost
                else:
                    best_sol = solution if cost < best_cost else best_sol
                    best_cost = cost if cost < best_cost else best_cost
            iteration += 1
        return best_sol, best_cost, iteration, time.time() - start_time



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("-> Usage: python3 grasp.py FILE_NAME SECONDS_MAX")
    else:
        inst = pickle.load(open(sys.argv[1], 'rb'))
        print("> GRASP ALGORITHM + LOCAL SEARCH")
        alpha = 0.1
        for _ in range(1,6):
            solver = Grasp(instance=inst, alpha=alpha, seconds=int(sys.argv[2]))
            sol, cost , it, tim = solver.solve()
            print("Result cost: %f, Time: %f , Alpha: %f, Iterations: %d" % ((cost, tim, alpha, it)))
            alpha += 0.1
