from greedy import Greedy
from grasp import Grasp
import pickle
from instance import Instance
import sys


algorithms = {'greedy': Greedy , 'grasp': Grasp}


def gen_instance():
    return pickle.load(open('instances/new_instance.pkl', 'rb'))


def solve_instance(instance, algorithm):
    inst = pickle.load(open('instances/new_instance.pkl', 'rb'))
    try:
        solver = algorithms[algorithm](inst)
        sol = solver.solve()
        print("""-> [ALGORITHM]: %s
->Solution: %s
->Cost: %d""" % ((algorithm, sol[0], sol[1])))
    except ValueError:
        print("[ERROR] Use Greedy + Local Search, or Grasp + Local_search")
        sys.exit(1)


def main():
    instance = gen_instance()
    solve_instance(instance, 'grasp')
    solve_instance(instance,'greedy')


if __name__ == "__main__":
    main()
