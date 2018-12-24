from bus import Buses
from drivers import Drivers
from services import Services
from restrictions import check_restrictions


class Instance:
    def __init__(self, bus_params, driver_params, service_params):
        self.buses = Buses(*bus_params)
        self.drivers = Drivers(*driver_params)
        self.services = Services(*service_params)

    def to_string(self):
        return """%s
    %s
    %s
        """ % ((self.buses.to_string(),
                self.drivers.to_string(),
                self.services.to_string()))

    def write_file(self, file_name):
        str = self.to_string()
        with open("instances/%s" % file_name, "w") as f:
            f.write(str)


if __name__ == "__main__":
    seed = 77
    bus_attributes = [seed, 10, 10, [10,20], [10,100], [10,100]]
    driver_attributes = [seed, 100, [10,100]]
    service_attributes = [seed, 6, [5,10], [5,10], [10,100], [5,10]]
    inst = Instance(bus_attributes,
                    driver_attributes,
                    service_attributes)

    inst.write_file("new_instance.dat")
