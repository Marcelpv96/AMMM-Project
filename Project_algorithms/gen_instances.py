import optparse
from services import Services
from drivers import Drivers
from bus import Buses
from instance import Instance


def gen_drivers(options):
    return Drivers(seed=int(options.seed),
                    num_drivers=int(options.num_drivers),
                    max_seconds=list(map(int, options.dmax.split(','))))


def gen_buses(options):
    return Buses(seed=int(options.seed),
                    number=int(options.num_buses),
                    max=int(options.bmax),
                    capacity=list(map(int, options.bcap.split(','))),
                    cost_min=list(map(int, options.bmin.split(','))),
                    cost_km=list(map(int, options.bkm.split(','))))


def gen_services(options):
    return Services(seed=int(options.seed),
                    number=int(options.num_services),
                    time=list(map(int, options.ss.split(','))),
                    duration_min=list(map(int, options.sd.split(','))),
                    duration_km=list(map(int, options.skm.split(','))),
                    num_passangers=list(map(int, options.sp.split(','))))


def generate_instance(options):
    print("- Hi! a new instance will be generated.")
    drivers = gen_drivers(options)
    print("**** GENERATING DRIVERS ****")
    for d in drivers.drivers:
        print(d)
    buses = gen_buses(options)
    print()
    print("**** GENERATING BUSES ****")
    for b in buses.buses:
        print(b)
    services = gen_services(options)
    print()
    print("**** GENERATING SERVICES ****")
    for s in services.services:
        print(s)
    instance = Instance(buses=buses,
                        drivers=drivers,
                        services=services,
                        bm=int(options.bm),
                        cbm=float(options.cbm),
                        cem=float(options.cem))
    print()
    file_name = 'instance_seed_%s'% options.seed
    feasible = True
    print([sum(l) for l in instance.services.overlaps])
    for services_overlaps in [sum(l) for l in instance.services.overlaps]:
        if services_overlaps > len(instance.drivers.drivers) and services_overlaps > len(instance.buses.max):
            feasible = False
    if feasible:
        print("It will be a feasible instance.")
    else:
        print("It will be a not feasible instance.")
    print("Writing all information int a file named : %s." % file_name)
    instance.write_file(file_name)


if __name__ =="__main__":
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter())

    parser.add_option('--seed', '--seed', action='store', default='27',
                      help='Seed.')

    parser.add_option('--bm', '--bm', action='store', default='250',
                  help='Bm value.')
    parser.add_option('--cbm', '--cbm', action='store', default='0.5',
                  help='Cbm value.')
    parser.add_option('--cem', '--cem', action='store', default='0.8',
                help='Cem value.')



    parser.add_option('--ss', '--service_start', action='store', default='0,5000',
                        help='Service start time, interval value.')
    parser.add_option('--skm', '--service_km', action='store', default='30, 60',
                        help='Service km duration, interval value.')
    parser.add_option('--sd', '--service_duration', action='store', default='60, 120',
                        help='Service duration time, interval value.')
    parser.add_option('--sp', '--service_passangers', action='store', default='20, 100',
                        help='Service num passangers, interval value.')

    parser.add_option('-b', '--num_buses', action='store', default='18',
                      help='Number of busses.')
    parser.add_option('-d', '--num_drivers', action='store', default='10',
                      help='Number of drivers.')
    parser.add_option('-s', '--num_services', action='store', default='28',
                        help='Number of services.')

    parser.add_option('--dmax', '--max_duration', action='store', default='120, 240 ',
                        help='Distance maxim that one driver can drive, interval value.')

    parser.add_option('--bmax', '--max_buses', action='store', default='6',
                        help='Number maxim of buses.')
    parser.add_option('--bmin', '--bus_cost_min', action='store', default='1, 15',
                        help='Cost each bus, by min, interval value.')
    parser.add_option('--bkm', '--bus_cost_km', action='store', default='1, 30',
                        help='Cost each bus, by km, interval value.')
    parser.add_option('--bcap', '--bus_capacity', action='store', default='100, 140',
                        help='Capacity of each bus, interval value.')
    (options, args) = parser.parse_args()
    generate_instance(options)
