import random
from utils import *

class One_service:
    def __init__(self, time, km, min, passangers):
        self.time = random.randint(time[0], time[1])
        self.km = random.randint(km[0], km[1])
        self.min = random.randint(min[0], min[1])
        self.passangers = random.randint(passangers[0], passangers[1])
        self.end = self.time + self.min


class Services:
    def __init__(self, seed, number, time, duration_min,
                duration_km, num_passangers):
        random.seed(seed)
        self.services = [One_service(time,
                                    duration_km,
                                    duration_min,
                                    num_passangers) for _ in range(0, number)]
        self.number = number
        self.overlaps = self.get_overlaps()

    def get_overlaps(self):
        overlaps = []
        for s1 in range(0, len(self.services)):
            overlaps += [[1 if self.services[s2].time < self.services[s1].end else 0 for s2 in range(0, len(self.services))]]
        return overlaps

    def get_starting_time(self):
        return [service.time for service in self.services]

    def get_duration_min(self):
        return [service.min for service in self.services]

    def get_duration_km(self):
        return [service.km for service in self.services]

    def get_num_passangers(self):
        return [service.passangers for service in self.services]

    def get_overlap_time(self):
        def process_lists(lists):
            result = ""
            for l in lists:
                result += """
                """
                result += "[%s]" %  " ".join(list(map(str, l)))
            return result
        return """[
        %s
        ]""" %  process_lists(self.overlaps)

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
    s = Services(10, 10, [1,10], [1,10], [1,10], [1,10])
    print(s.to_string())
