import pickle
import math
from instance import Instance
from copy import deepcopy
from solution import Candidate, Solution
from restrictions import Restrictions
from solver import Solver
from local_search import Local_search
import time


class Greedy(Solver):

    def selection_function(self, candidates, partial_solution):
        best_cost = math.inf
        best_candidate = None
        for candidate in candidates:
            candidate_cost = candidate.get_cost(partial_solution, self.instance)
            if candidate_cost < best_cost:
                best_candidate = candidate
                best_cost = candidate_cost
        return best_candidate

    def solve(self):
        partial_solution = []
        print("Start get candidates")
        services = self.instance.services.services
        print(len(services))
        start_time = time.time()
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
        if not solution.is_valid():
            return None, -1, -1
        if solution.get_cost() == math.inf:
            return None, -1, -1
        ls = Local_search(solution)
        solution, cost = ls.run()
        return solution, cost, (time.time() - start_time)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("-> Usage: python3 greedy.py FILE_NAME ")
    else:
        inst = pickle.load(open(sys.argv[1], 'rb'))
        print("> GREEDY ALGORITHM + LOCAL SEARCH")
        solver = Greedy(inst)
        sol, cost, tim = solver.solve()
        print(sol)
        print("Result cost: %f, Time: %f "% ((cost, tim)))
