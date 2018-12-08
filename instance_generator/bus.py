import random


class Bus:
    def __init__(self, seed, number, max, capacity, cost_min, cost_km):
        random.seed(seed)
        self.number = number
        self.max = max
        self.capacity = [random.randint(capacity[0], capacity[1]) for _ in range(0, number)]
        self.cost_min = self.get_cost(cost_min, number)
        self.cost_km = self.get_cost(cost_km, number)

    def get_cost(self, cost, number):
        costs = [random.randint(cost[0], cost[1]) for _ in range(0, number)]
        result = "[%s]" % " ".join(list(map(str,costs)))
        return result

    def str_capacity(self):
        return "[%s]" % " ".join(list(map(str, self.capacity)))

    def to_string(self):
        return """nBuses=%d;
max_busses=%d;
cap_B=%s;
euros_min_B=%s;
euros_km_B=%s;
""" % ((self.number, self.max, self.str_capacity(), self.cost_min, self.cost_km))


if __name__ == "__main__":
    b = Bus(10, 10, 10, [5, 10], [1,10], [1,10])
    print(b.to_string())
