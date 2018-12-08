import random


class One_service:
    def __init__(self, time, km, min, passangers):
        self.time = time
        self.km = km
        self.min = min
        self.passangers = passangers
        self.end = time + min


class Services:
    def __init__(self, seed, number, time, duration_min, duration_km, num_passangers):
        random.seed(seed)
        self.services = Services.gen_services(number, time, duration_km, duration_min, num_passangers)
        self.overlaps = self.get_overlaps(self.services)

    @staticmethod
    def gen_services(number, time, duration_km, duration_min, num_passangers):
        services = []
        for _ in range(0, number):
            start_time = random.randint(time[0], time[1])
            km = random.randint(duration_km[0], duration_km[1])
            min = random.randint(duration_min[0], duration_min[1])
            passangers = random.randint(num_passangers[0], num_passangers[1])
            services += [One_service(start_time, km, min, passangers)]
        return services

    def get_overlaps(self, services):
        overlaps = []
        for s1 in range(0, len(services)-1):
            overlaps += [[1 if services[s2].time < services[s1].end else 0 for s2 in range(0, len(services)-1)]]
        return overlaps

    def get_starting_time(self):
        return "[%s]" %  " ".join(list(map(str, [service.time for service in self.services])))

    def get_duration_min(self):
        return "[%s]" %  " ".join(list(map(str, [service.min for service in self.services])))

    def get_duration_km(self):
        return "[%s]" %  " ".join(list(map(str, [service.km for service in self.services])))

    def get_overlap_time(self):
        return "[%s]" %  " ".join(list(map(str, [service.time for service in self.services])))

    def get_num_passangers(self):
        return "[%s]" %  " ".join(list(map(str, [service.passangers for service in self.services])))

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
overlap_time=%s;
num_passangers=%s;""" % ((len(self.services), self.get_starting_time(), self.get_duration_min(), self.get_duration_km(),
                        self.get_overlap_time(), self.get_num_passangers()))


if __name__ == "__main__":
    s = Services(10, 10, [1,10], [1,10], [1,10], [1,10])
    print(s.to_string())
