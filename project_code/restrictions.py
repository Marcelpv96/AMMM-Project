from copy import deepcopy


def check_capacity_available_requested(instance):
    available_capacity = sum((bus.capacity for bus in instance.buses.buses))
    requested_capacity = sum((service.passangers for service in instance.services.services))
    return available_capacity*0.75 >= requested_capacity

def check_duration_available_requested(instance):
    available_time = sum((driver.max_seconds for driver in instance.drivers.drivers))
    requested_time = sum((service.min for service in instance.services.services))
    max_available = max((driver.max_seconds for driver in instance.drivers.drivers))
    max_requested = max((service.min for service in instance.services.services))
    return available_time*0.75 >= requested_time and  max_available >= max_requested


def check_restrictions(instance):
    return check_duration_available_requested(instance) and check_capacity_available_requested(instance)


class Restrictions:

    @staticmethod
    def restriction_1(candidate, partial_solution, overlaps):
        for assignament in partial_solution:
            if assignament.driver  == candidate.driver and overlaps[assignament.service.id][candidate.service.id]:
                return False
        return True

    @staticmethod
    def restriction_2(candidate, partial_solution, overlaps):
        for assignament in partial_solution:
            if assignament.bus == candidate.bus and overlaps[assignament.service.id][candidate.service.id]:
                return False
        return True

    @staticmethod
    def restriction_3(candidate, partial_solution, max_buses):
        sol = deepcopy(partial_solution)
        sol = partial_solution + [candidate]
        buses = {assignament.bus.id for assignament in sol}
        return len(buses) <= max_buses

    @staticmethod
    def restriction_4(candidate, partial_solution):
        return not candidate in partial_solution

    @staticmethod
    def restriction_5(candidate, partial_solution):
        for assignament in partial_solution:
            if candidate.service == assignament.service:
                return False
        return True

    @staticmethod
    def restriction_6(candidate, partial_solution):
        mins = candidate.service.min
        driver = candidate.driver
        for assignament in partial_solution:
            if driver == assignament.driver:
                mins += assignament.service.min
        return mins <= driver.max_seconds

    @staticmethod
    def restriction_7(candidate, partial_solution):
        used = 0
        cap = candidate.bus.capacity
        for assig in partial_solution:
            if candidate.bus == assig.bus:
                used += assig.service.passangers
        return used + candidate.service.passangers <= cap

    @staticmethod
    def check_all(candidate, partial_solution, overlaps, max_buses):
        return Restrictions.restriction_1(candidate, partial_solution, overlaps) and\
                Restrictions.restriction_2(candidate, partial_solution, overlaps) and\
                Restrictions.restriction_3(candidate, partial_solution, max_buses) and\
                Restrictions.restriction_4(candidate, partial_solution) and\
                Restrictions.restriction_5(candidate, partial_solution) and\
                Restrictions.restriction_6(candidate, partial_solution) and\
                Restrictions.restriction_7(candidate, partial_solution)



if __name__ == "__main__":
    bus_attributes = [100, 100, 100, [50,100], [10,100], [10,100]]
    driver_attributes = [100, 100, [10,100]]
    service_attributes = [100, 100, [10,100], [10,100], [10,100], [10,100]]
    instance = Instance(bus_attributes,
                    driver_attributes,
                    service_attributes)
    print(check_capacity_available_requested(instance))
    print(check_duration_available_requested(instance))
