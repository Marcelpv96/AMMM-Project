from solution import Candidate, Solution
from instance import Instance
import math


class Solver:
    def __init__(self, inst):
        self.instance = inst

    def get_candidates(self):
        drivers = self.instance.drivers.drivers
        buses = self.instance.buses.buses
        services = self.instance.services.services
        candidates = []
        for service in services:
            for bus in buses:
                for driver in drivers:
                        candidates += [Candidate(service, bus, driver)]
        return candidates

    def objective_function(self, solution):
        return solution.get_cost()

    def solution_function(self, partial_solution):
        services_done = [assignament.service for assignament in partial_solution]
        for service in self.instance.services.services:
            if service not in services_done:
                return False
        return True

    def update_candidates(self, candidates, partial_solution):
        return list(filter(lambda x: x.get_cost(partial_solution, self.instance) < math.inf, candidates))
