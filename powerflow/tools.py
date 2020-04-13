from .systemclass import SystemClass
from .formatters import __get_mag_vanish, __get_ang_vanish
from .formatters import __identify_ph_config


def __verify_bus_list(distSys: SystemClass, buses: list):
    all_bus_names = distSys.get_all_bus_names()
    verify_per_bus = list(map(lambda bus: bus in all_bus_names, buses))
    return verify_per_bus


def __get_bus_v_pu_ang(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.puVmagAngle()


def __get_bus_ph(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.Nodes()


def __get_bus_v_pu(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    v_pu = __get_mag_vanish(list_ph, v_pu_ang_dss)
    return v_pu


def __get_bus_ang(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    ang = __get_ang_vanish(list_ph, v_pu_ang_dss)
    return ang


def __get_all_v_pu(distSys: SystemClass):
    all_bus_names = distSys.get_all_bus_names()
    all_v_pu = []
    for bus in all_bus_names:
        v_pu = __get_bus_v_pu(distSys, bus)
        all_v_pu.append(v_pu)

    return all_v_pu


def __get_all_ang(distSys: SystemClass):
    all_bus_names = distSys.get_all_bus_names()
    all_ang = []
    for bus in all_bus_names:
        ang = __get_bus_ang(distSys, bus)
        all_ang.append(ang)

    return all_ang


def __get_all_num_ph(distSys: SystemClass):
    all_bus_names = distSys.get_all_bus_names()
    all_num_ph = []
    for bus in all_bus_names:
        ph = __get_bus_ph(distSys, bus)
        ph_config = __identify_ph_config(ph)

        all_num_ph.append(ph_config)

    return all_num_ph
