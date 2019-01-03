import pickle
import math
from instance import Instance
from copy import deepcopy
from solution import Candidate, Solution
from restrictions import Restrictions
import random
from solver import Solver
from local_search import Local_search


class Grasp(Solver):
    def __init__(self, instance, alpha=0.5, seed=96):
        self.instance = instance
        self.alpha = alpha
        random.seed(seed)

    def RCL(self, candidates_cost):
        q_max = candidates_cost[-1][1]
        q_min = candidates_cost[0][1]
        RCLmax = q_max - self.alpha*(q_max - q_min)
        nearest_value = min((cost[1] for cost in candidates_cost), key=lambda x:abs(x-RCLmax))
        return[candidate[0] for candidate in filter(lambda y: y[1] <= nearest_value, candidates_cost)]

    def selection_function(self, candidates, partial_solution):
        candidates_cost = [(candidate ,candidate.get_cost(partial_solution, self.instance)) for candidate in candidates]
        candidates_cost.sort(key=lambda x: x[1])
        candidates = [candidate[0] for candidate in candidates_cost]
        RCL = self.RCL(candidates_cost)
        return RCL[random.randint(0, len(RCL)-1)]

    def solve(self):
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
        if not solution.is_valid():
            return None, -1
        if solution.get_cost() == math.inf:
            return None, -1
        ls = Local_search(solution)
        solution, cost = ls.run()
        return solution, cost



if __name__ == "__main__":
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    solver = Grasp(inst)
    print(solver.solve())
