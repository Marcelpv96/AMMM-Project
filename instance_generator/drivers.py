import random
from utils import *


class One_driver:
    def __init__(self, max_seconds):
        self.max_seconds = random.randint(max_seconds[0], max_seconds[1])


class Drivers:
    def __init__(self, seed, num_drivers, max_seconds):
        random.seed(seed)
        self.number = num_drivers
        self.drivers = [One_driver(max_seconds) for _ in range(0, num_drivers)]

    def get_max(self):
        return [driver.max_seconds for driver in self.drivers]

    def to_string(self):
        return """
        nDrivers=%d;
        max_D=%s;
        """ % ((self.number, list_str(self.get_max())))


if __name__ == "__main__":
    d = Drivers(10, 10, [1,10])
    print(d.to_string())
