from greedy import Greedy
from grasp import Grasp
import pickle
from instance import Instance
import sys
import os


algorithms = {'greedy': Greedy , 'grasp': Grasp}


def gen_instance(seed):
    return pickle.load(open(os.path.join('instances', 'instance_seed_%s.pkl' % seed), 'rb'))


def solve_instance(instance, algorithm):
    inst = instance
    try:
        solver = algorithms[algorithm](inst)
        sol = solver.solve()
        print("""-> [ALGORITHM]: %s
->Cost: %d""" % ((algorithm, sol[1])))
    except ValueError:
        print("[ERROR] Use Greedy + Local Search, or Grasp + Local_search")
        sys.exit(1)


def main(instance):
    solve_instance(instance, 'grasp')
    solve_instance(instance,'greedy')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('> USAGE, put the seed of your instance as: python3 main.py SEED_NUMBER')
    else:
        print("> Hi! now a greedy algorithm + LS and grasp algorithm + LS will look for a solution of instance : <%s>. "%sys.argv[1])
        instance = gen_instance(sys.argv[1])
        main(instance)
