import random
from utils import *


class One_service:
    def __init__(self, time, km, min, passangers, id):
        self.time = random.randint(time[0], time[1])
        self.km = random.randint(km[0], km[1])
        self.min = random.randint(min[0], min[1])
        self.passangers = random.randint(passangers[0], passangers[1])
        self.end = self.time + self.min
        self.id = id

    def __eq__(self, other_service):
        return self.id == other_service.id

    def __str__(self):
        return "-> [Service] id: %d " % ((self.id))


class Services:
    def __init__(self, seed, number, time, duration_min,
                duration_km, num_passangers):
        random.seed(random.random())
        self.services = [One_service(time,
                                    duration_km,
                                    duration_min,
                                    num_passangers,
                                    id) for id in range(0, number)]
        self.number = number
        self.overlaps = self.get_overlaps()

        print(self.overlaps)


    def get_overlaps(self):
        overlaps = [[0 for _ in range(0, len(self.services))] for _ in range(0, len(self.services))]
        for s1 in range(0, len(self.services)):
            for s2 in range(0, len(self.services)):
                print((self.services[s2].time ,self.services[s1].time ))
                if self.services[s1].time <= self.services[s2].time and self.services[s1].end >= self.services[s2].time and s1 != s2:
                    overlaps[s1][s2] = 1
                    overlaps[s2][s1] = 1
        return overlaps

    def get_starting_time(self):
        return [service.time for service in self.services]

    def get_duration_min(self):
        return [service.min for service in self.services]

    def get_duration_km(self):
        return [service.km for service in self.services]

    def get_num_passangers(self):
        return [service.passangers for service in self.services]

    def to_string(self):
        return """
nServices=%d;
S_starting_time=%s;
duration_s_min=%s;
duration_s_km=%s;
num_passangers=%s;""" % ((self.number,
                        list_str(self.get_starting_time()),
                        list_str(self.get_duration_min()),
                        list_str(self.get_duration_km()),
                        list_str(self.get_num_passangers())))


if __name__ == "__main__":
    s = Services(2, 2, [1,10], [1,10], [1,10], [1,10])
    s1 = s.services[0]
    s2 = s.services[1]
    print(s1 == s1)
