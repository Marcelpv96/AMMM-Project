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
        mins = candidate.mins
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

    def get_cost(self, partial_solution, instance):
        if self.feasible_candidate(partial_solution, instance):
            cost = 0
            cost += self.bus.cost_min * self.service.min
            cost += self.bus.cost_km * self.service.km
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


class Greedy:
    def __init__(self, inst):
        self.candidates = self.get_candidates(inst.services.services,
                                             inst.buses.buses,
                                             inst.drivers.drivers)
        self.instance = inst

    def selection_function(self, candidates, partial_solution):
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

    def feasible_solution(self, partial_solution, candidate):
        pass


if __name__ == "__main__":
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    solver = Greedy(inst)
    candidates = solver.candidates

    partial_solution = [candidates[0]]
    candidate = candidates[1]
    print(candidate.get_cost(partial_solution, inst))
