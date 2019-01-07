from bus import Buses
from drivers import Drivers
from services import Services
from restrictions import check_restrictions
import pickle


class Instance:
    def __init__(self, buses, drivers, services, bm, cbm, cem):
        self.buses = buses
        self.drivers = drivers
        self.services = services
        self.overlaps = self.services.overlaps
        self.BM = bm
        self.CBM = cbm
        self.CEM = cem
        self.max_buses = buses.max

    def to_string(self):
        return """%s
%s
%s
BM=%d;
CBM=%f;
CEM=%f;    """ % ((self.buses.to_string(),
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
