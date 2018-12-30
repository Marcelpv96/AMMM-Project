from bus import Buses
from drivers import Drivers
from services import Services
from restrictions import check_restrictions
import pickle


class Instance:
    def __init__(self, bus_params, driver_params, service_params):
        self.buses = Buses(*bus_params)
        self.drivers = Drivers(*driver_params)
        self.services = Services(*service_params)
        self.overlaps = self.services.overlaps
        self.max_buses = self.buses.max
        self.BM = 10
        self.CBM = 20
        self.CEM = 30

    def to_string(self):
        return """%s
%s
%s
BM=%d
CBM=%d
CEM=%d    """ % ((self.buses.to_string(),
                self.drivers.to_string(),
                self.services.to_string(),
                self.BM,
                self.CBM,
                self.CEM))

    def write_file(self, file_name):
        str = self.to_string()
        with open("instances/%s.dat" % file_name, "w") as f:
            f.write(str)
        pickle.dump(self, open("instances/%s.pkl" % file_name, 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    seed = 77
    bus_attributes = [seed, 2, 10, [10,20], [10,100], [10,100]]
    driver_attributes = [seed, 2, [10,100]]
    service_attributes = [seed, 2, [5,10], [5,10], [10,100], [5,10]]
    inst = Instance(bus_attributes,
                    driver_attributes,
                    service_attributes)

    inst.write_file("new_instance")
