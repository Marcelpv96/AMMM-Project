"""
∙ Instance example:

    - Sumatori capacitat de busos ha de ser mes gran que el sumatori de busos.
    - No pot haver cap servei que sigo de mes durada que el maxim d'hores que pot fer un driver.

"""

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


if __name__ == "__main__":
    bus_attributes = [100, 100, 100, [50,100], [10,100], [10,100]]
    driver_attributes = [100, 100, [10,100]]
    service_attributes = [100, 100, [10,100], [10,100], [10,100], [10,100]]
    instance = Instance(bus_attributes,
                    driver_attributes,
                    service_attributes)
    print(check_capacity_available_requested(instance))
    print(check_duration_available_requested(instance))
