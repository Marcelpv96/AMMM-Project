from bus import Bus
from drivers import Drivers
from services import Services


def get_bus_drivers_services():
    b = Bus(100, 100, 100, [50,100], [10,100], [10,100])
    d = Drivers(100, 100, [10,100])
    s = Services(100, 100, [10,100], [10,100], [10,100], [10,100])
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
