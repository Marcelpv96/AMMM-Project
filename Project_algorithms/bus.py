import random
from utils import *


class One_bus:
    def __init__(self, capacity, cost_min, cost_km, id):
        self.capacity = random.randint(capacity[0], capacity[1])
        self.cost_min = random.uniform(cost_min[0], cost_min[1])
        self.cost_km = random.uniform(cost_km[0], cost_km[1])
        self.id = id

    def __eq__(self, other_bus):
        return self.id == other_bus.id

    def __str__(self):
        return "-> [Bus] id: %d" % ((self.id))


class Buses:
    def __init__(self, seed, number, max, capacity, cost_min, cost_km):
        random.seed(random.random())
        self.number = number
        self.max = max
        self.buses = [One_bus(capacity, cost_min, cost_km, id) for id in range(0, number)]

    def get_capacity(self):
        return [bus.capacity for bus in self.buses]

    def get_cost_min(self):
        return [bus.cost_min for bus in self.buses]

    def get_cost_km(self):
        return [bus.cost_km for bus in self.buses]

    def to_string(self):
        return """nBuses=%d;
max_busses=%d;
cap_B=%s;
euros_min_B=%s;
euros_km_B=%s;
""" % ((self.number,
        self.max,
        list_str(self.get_capacity()),
        list_str(self.get_cost_min()),
        list_str(self.get_cost_km())
        ))


if __name__ == "__main__":
    b = Bus(10, 10, 10, [5, 10], [1,10], [1,10])
    print(b.to_string())
