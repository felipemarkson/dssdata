from .systemclass import SystemClass
from .formatters import __get_mag_vanish, __get_ang_vanish
from .formatters import __identify_ph_config
from .decorators import pf_tools

"""
TODO:   Remover todos os __verifys e utilizar .formatters.__check_elements
        Ex: Veja reg_tools.py
"""


@pf_tools
def __verify_bus_list(distSys: SystemClass, buses: list):
    all_bus_names = distSys.get_all_bus_names()
    verify_per_bus = list(map(lambda bus: bus in all_bus_names, buses))
    return verify_per_bus


@pf_tools
def __get_bus_v_pu_ang(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.puVmagAngle()


@pf_tools
def __get_bus_ph(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.Nodes()


@pf_tools
def __get_bus_v_pu(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    v_pu = __get_mag_vanish(list_ph, v_pu_ang_dss)
    return v_pu


@pf_tools
def __get_bus_ang(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    ang = __get_ang_vanish(list_ph, v_pu_ang_dss)
    return ang


@pf_tools
def __get_all_v_pu(distSys: SystemClass) -> list:

    return list(
        map(
            lambda bus: __get_bus_v_pu(distSys, bus),
            distSys.get_all_bus_names(),
        )
    )


@pf_tools
def __get_all_ang(distSys: SystemClass) -> list:
    return list(
        map(
            lambda bus: __get_bus_ang(distSys, bus),
            distSys.get_all_bus_names(),
        )
    )


@pf_tools
def __get_all_num_ph(distSys: SystemClass) -> list:

    return list(
        map(
            lambda bus: __identify_ph_config(__get_bus_ph(distSys, bus)),
            distSys.get_all_bus_names(),
        )
    )
