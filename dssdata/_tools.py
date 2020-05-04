from . import SystemClass
from ._formatters import (
    __get_mag_vanish,
    __get_ang_vanish,
    __identify_ph_config,
)
from .decorators import pf_tools


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
def __get_all_v_pu(distSys: SystemClass) -> tuple:

    return tuple(
        map(
            lambda bus: __get_bus_v_pu(distSys, bus),
            distSys.get_all_bus_names(),
        )
    )


@pf_tools
def __get_all_ang(distSys: SystemClass) -> tuple:
    return tuple(
        map(
            lambda bus: __get_bus_ang(distSys, bus),
            distSys.get_all_bus_names(),
        )
    )


@pf_tools
def __get_all_num_ph(distSys: SystemClass) -> tuple:

    return tuple(
        map(
            lambda bus: __identify_ph_config(__get_bus_ph(distSys, bus)),
            distSys.get_all_bus_names(),
        )
    )
