from instance import Instance
from restrictions import Restrictions
from copy import deepcopy
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

    def get_bus_minkm(self):
        return self.bus.cost_min + self.bus.cost_km

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

    def get_driver_mins(self, partial_solution):
        sol = deepcopy(partial_solution)
        try:
            sol.remove(self)
        except ValueError:
            sol += [self]
        minwork = [0 if assignment.driver != self.driver else assignment.service.min for assignment in sol]
        mins_work = sum(minwork) + self.service.min
        return mins_work

    def __eq__(self, other_candidate):
        return self.service == other_candidate.service and\
                self.bus == other_candidate.bus and\
                self.driver == other_candidate.driver

    def __str__(self):
        return "(*) Service: %s, bus: %s, driver: %s " % ((self.service, self.bus, self.driver))


class Solution:
    def __init__(self, candidates_list, instance):
        self.assignments = candidates_list
        self.instance = instance

    def get_driver_cost(self):
        drivers = []
        assignments = []
        cost = 0
        for assignment in self.assignments:
            if assignment.driver not in drivers:
                drivers += [assignment.driver]
                assignments += [assignment]
        for assignment in assignments:
            mins = assignment.get_driver_mins(self.assignments)
            if mins <= self.instance.BM:
                cost += mins * self.instance.CBM
            else:
                cost += self.instance.BM * self.instance.CBM + (mins - self.instance.BM) * self.instance.CEM
        return cost

    def get_cost(self):
        return self.get_driver_cost() + sum((assignment.get_bus_cost() for assignment in self.assignments))

    def sort_assignments(self):
        assignments = deepcopy(self.assignments)
        assig_driver_hours = [assig.get_driver_mins(self.assignments) for assig in assignments]
        sorted_assignments = list(zip(assignments, assig_driver_hours))
        sorted_assignments.sort(key=lambda x: x[1] - self.instance.BM)
        return sorted_assignments

    def sort_by_bus_cost(self):
        assignments = deepcopy(self.assignments)
        assig_bus_cost = [assig.get_bus_minkm() for assig in assignments]
        sorted_assignments = list(zip(assignments, assig_bus_cost))
        sorted_assignments.sort(key=lambda x:x[1])
        return sorted_assignments


    def is_valid(self):
        services = self.instance.services.services
        services_assig = [assignment.service for assignment in self.assignments]
        for service in services:
            if service not in services_assig:
                return False
        return True


    def __str__(self):
        return "\n".join(map(str, self.assignments))
