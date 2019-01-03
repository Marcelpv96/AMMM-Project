import pickle
import math
from instance import Instance
from copy import deepcopy
from solution import Candidate, Solution
from restrictions import Restrictions
from solver import Solver
from local_search import Local_search


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
    solver = Greedy(inst)
    sol = solver.solve()
    print(sol)
    print(sol[0])
