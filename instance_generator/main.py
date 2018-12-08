from bus import Bus
from drivers import Drivers
from services import Services


def get_bus_drivers_services():
    b = Bus(10, 10, 10, [5,10], [1,10], [1,10])
    d = Drivers(10, 10, [1,10])
    s = Services(10, 10, [1,10], [1,10], [1,10], [1,10])
    return b, d, s

def to_string(buses, drivers, services):
    return """%s
%s
%s
    """ % ((buses.to_string(), drivers.to_string(), services.to_string()))

def write_file(str, file_name):
    with open("instances/%s" % file_name, "w") as f:
        f.write(str)


def main():
    b_d_s = get_bus_drivers_services()
    str = to_string(*b_d_s)
    write_file(str, "instance1.dat")

if __name__ == "__main__":
    main()
