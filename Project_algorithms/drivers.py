import random
from utils import *


class One_driver:
    def __init__(self, max_seconds, id):
        self.max_seconds = random.randint(max_seconds[0], max_seconds[1])
        self.id = id

    def __eq__(self, other_driver):
        return self.id == other_driver.id

    def __str__(self):
        return "-> [Driver] ID : %d " % ((self.id))


class Drivers:
    def __init__(self, seed, num_drivers, max_seconds):

        random.seed(random.random())
        self.number = num_drivers
        self.drivers = [One_driver(max_seconds, id) for id in range(0, num_drivers)]

    def get_max(self):
        return [driver.max_seconds for driver in self.drivers]

    def to_string(self):
        return """
nDrivers=%d;
max_D=%s;
        """ % ((self.number, list_str(self.get_max())))


if __name__ == "__main__":
    d = Drivers(10, 10, [1,10])
    d0 = d.drivers[0]
    d1 = d.drivers[1]
