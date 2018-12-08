import random


class Drivers:
    def __init__(self, seed, num_drivers, max_seconds):
        random.seed(seed)
        self.num_drivers = num_drivers
        self.max_seconds = self.get_max(max_seconds, num_drivers)

    def get_max(self, max_seconds, number):
        max_D = [random.randint(max_seconds[0], max_seconds[1]) for _ in range(0, number)]
        result = "[%s]" % " ".join(list(map(str, max_D)))
        return result

    def to_string(self):
        return"""
nDrivers=%d;
max_D=%s;
        """ % ((self.num_drivers, self.max_seconds))


if __name__ == "__main__":
    d = Drivers(10, 10, [1,10])
    print(d.to_string())
