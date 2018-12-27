from instance import Instance
from restrictions import Restrictions
import math


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
