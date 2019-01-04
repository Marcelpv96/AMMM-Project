import pickle
from instance import Instance
import math
from copy import deepcopy
from solution import Candidate, Solution


class Local_search:

    def __init__(self, initial_sol):
        self.instance = initial_sol.instance
        self.initial_sol = initial_sol
        self.initial_cost = initial_sol.get_cost()

    def neighbour_bus(self, initial_sol):
        alternative_solutions = []
        for assig1 in initial_sol.assignments:
            for assig2 in initial_sol.assignments:
                if assig1 != assig2 and initial_sol.intance.services.overlaps[assig1.]:




                    
                    alternative_sol = deepcopy(initial_sol.assignments)
                    alternative_sol.remove(assig1)
                    new_candidate = Candidate(assig1.service, assig2.bus, assig1.driver)
                    if new_candidate.feasible_candidate(alternative_sol, initial_sol.instance):
                        alternative_sol += [new_candidate]
                        alternative_solutions += [Solution(deepcopy(alternative_sol), initial_sol.instance)]
        return min(alternative_solutions, key = lambda x: x.get_cost())

    def neighbour_driver(self, initial_sol):
        alternative_solutions = []
        Sorted_assigs = [assig for assig, cost in initial_sol.sort_assignments()]
        Reverse_assigs = deepcopy(Sorted_assigs)
        Reverse_assigs.reverse()
        for assig1 in Sorted_assigs:
            for assig2 in Reverse_assigs:
                new_assig = Candidate(assig2.service, assig2.bus, assig1.driver)
                new_partial_sol = deepcopy(Reverse_assigs)
                new_partial_sol.remove(assig2)
                if new_assig.feasible_candidate(new_partial_sol, self.instance):
                    new_partial_sol += [assig2]
                    new_solution = Solution(new_partial_sol, self.instance)
                    cost = new_solution.get_cost()
                else:
                    new_partial_sol += [assig2]
                    new_solution = Solution(new_partial_sol, self.instance)
                    cost = math.inf
                alternative_solutions += [(new_solution, cost)]
        return min(alternative_solutions, key = lambda x: x[1])

    def get_neighbourhoods(self, initial_sol):
        best_buses_combination = self.neighbour_bus(initial_sol)
        best_neighbour = self.neighbour_driver(best_buses_combination)
        return best_neighbour


    def run(self):
        ini_sol = self.initial_sol
        ini_cost = self.initial_cost
        obtained_cost = math.inf
        best_sol = ini_sol
        while ini_cost < obtained_cost:
            best_sol, obtained_cost = self.get_neighbourhoods(ini_sol)
            if best_sol == ini_sol:
                break;
            elif obtained_cost <= ini_cost:
                break;
            else:
                ini_cost = obtained_cost
                ini_sol = best_sol
        return best_sol, best_sol.get_cost()


if __name__ == "__main__":
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    greedy_solver = Greedy(inst)
    solution, cost = greedy_solver.solve()
    solution.get_cost()
    ls = Local_search(solution)
    print(ls.run())
