import pickle
import math
from instance import Instance
from copy import deepcopy
from solution import Candidate, Solution
from restrictions import Restrictions


class Greedy:
    def __init__(self, inst):
        self.instance = inst

    def selection_function(self, candidates, partial_solution, instance):
        best_cost = math.inf
        best_candidate = None
        for candidate in candidates:
            candidate_cost = candidate.get_cost(partial_solution, instance)
            if candidate_cost < best_cost:
                best_candidate = candidate
                best_cost = candidate_cost
        return best_candidate

    def get_candidates(self, services, buses, drivers):
        candidates = []
        for service in services:
            for bus in buses:
                for driver in drivers:
                        candidates += [Candidate(service, bus, driver)]
        return candidates

    def solution_function(self, partial_solution):
        services_done = [assignament.service for assignament in partial_solution]
        for service in self.instance.services.services:
            if service not in services_done:
                return False
        return True

    def objective_function(self, solution):
        return solution.get_cost()

    def solve(self):
        partial_solution = []
        candidates = self.get_candidates(self.instance.services.services,
                                             self.instance.buses.buses,
                                             self.instance.drivers.drivers)
        while not self.solution_function(partial_solution):
            candidate = self.selection_function(candidates, partial_solution, self.instance)
            partial_solution += [candidate]
        solution = Solution(partial_solution, self.instance)
        return solution, self.objective_function(solution)


if __name__ == "__main__":
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    solver = Greedy(inst)
    sol = solver.solve()
    print(sol[0])
