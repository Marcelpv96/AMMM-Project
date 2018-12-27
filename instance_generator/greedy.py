import pickle
import math
from instance import Instance
from copy import deepcopy


class Restrictions:

    @staticmethod
    def restriction_1(candidate, partial_solution, overlaps):
        for assignament in partial_solution:
            if assignament.driver  == candidate.driver and overlaps[assignament.service.id][candidate.service.id]:
                return False
        return True

    @staticmethod
    def restriction_2(candidate, partial_solution, overlaps):
        for assignament in partial_solution:
            if assignament.bus == candidate.bus and overlaps[assignament.service.id][candidate.service.id]:
                return False
        return True

    @staticmethod
    def restriction_3(candidate, partial_solution, max_buses):
        sol = deepcopy(partial_solution)
        sol = partial_solution + [candidate]
        buses = {assignament.bus.id for assignament in sol}
        return len(buses) <= max_buses

    @staticmethod
    def restriction_4(candidate, partial_solution):
        return not candidate in partial_solution

    @staticmethod
    def restriction_5(candidate, partial_solution):
        for assignament in partial_solution:
            if candidate.service == assignament.service:
                return False
        return True

    @staticmethod
    def restriction_6(candidate, partial_solution):
        mins = candidate.service.min
        driver = candidate.driver
        for assignament in partial_solution:
            if driver == assignament.driver:
                mins += assignament.service.min
        return mins <= driver.max_seconds

    @staticmethod
    def check_all(candidate, partial_solution, overlaps, max_buses):
        return Restrictions.restriction_1(candidate, partial_solution, overlaps) and\
                Restrictions.restriction_2(candidate, partial_solution, overlaps) and\
                Restrictions.restriction_3(candidate, partial_solution, max_buses) and\
                Restrictions.restriction_4(candidate, partial_solution) and\
                Restrictions.restriction_5(candidate, partial_solution) and\
                Restrictions.restriction_6(candidate, partial_solution)


class Candidate:
    def __init__(self, service, bus, driver):
        self.service = service
        self.bus = bus
        self.driver = driver

    def get_bus_cost(self):
        cost = 0
        cost += self.bus.cost_min * self.service.min
        cost += self.bus.cost_km * self.service.km
        return cost

    def minutes_drived(self):
        return self.service.min

    def get_cost(self, partial_solution, instance):
        if self.feasible_candidate(partial_solution, instance):
            cost = self.get_bus_cost()
            return cost
        else:
            cost = math.inf
            return cost

    def feasible_candidate(self, partial_solution, instance):
        return Restrictions.check_all(self, partial_solution, instance.overlaps, instance.max_buses)

    def __eq__(self, other_candidate):
        return self.service == other_candidate.service and\
                self.bus == other_candidate.bus and\
                self.driver == other_candidate.driver

    def __str__(self):
        return "(*) Service: %s, bus: %s, driver: %s " % ((self.service, self.bus, self.driver))


class Solution:
    def __init__(self, candidates_list, instance):
        self.solution_parts = candidates_list
        self.instance = instance

    def get_driver_cost(self):
        cost = 0
        for part1 in  self.solution_parts:
            mins = 0
            for part2 in self.solution_parts:
                if part1.driver == part2.driver:
                    mins += part2.minutes_drived()
            cost += 0 if 1>2 else -1
        return cost

    def get_cost(self):
        return self.get_driver_cost() + sum((solution_part.get_bus_cost() for solution_part in self.solution_parts))


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
        candidates = self.get_candidates(inst.services.services,
                                             inst.buses.buses,
                                             inst.drivers.drivers)
        while not self.solution_function(partial_solution):
            candidate = self.selection_function(candidates, partial_solution, self.instance)
            partial_solution += [candidate]
        solution = Solution(partial_solution, self.instance)
        return solution, self.objective_function(solution)


if __name__ == "__main__":
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    solver = Greedy(inst)
    sol = solver.solve()
    print(sol)
