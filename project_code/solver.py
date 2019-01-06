from solution import Candidate, Solution
from instance import Instance
from restrictions import Restrictions
import math


class Solver:
    def __init__(self, inst):
        self.instance = inst

    def get_candidates(self):
        services = self.instance.services.services
        drivers = self.instance.drivers.drivers
        buses = self.instance.buses.buses
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
        res = list(filter(lambda x: Restrictions.check_all(x, partial_solution, self.instance.services.overlaps, self.instance.buses.max), candidates))
        return res
