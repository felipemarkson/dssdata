from . import SystemClass
from ._formatters import (
    __get_mag_vanish,
    __get_ang_vanish,
)
from .decorators import tools


@tools
def __get_bus_v_pu_ang(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.puVmagAngle()


@tools
def __get_bus_ph(distSys: SystemClass, bus: str):
    distSys.dss.Circuit.SetActiveBus(bus)
    return distSys.dss.Bus.Nodes()


@tools
def __get_bus_v_pu(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    v_pu = __get_mag_vanish(list_ph, v_pu_ang_dss)
    return v_pu


@tools
def __get_bus_ang(distSys: SystemClass, bus: str):
    v_pu_ang_dss = __get_bus_v_pu_ang(distSys, bus)
    list_ph = __get_bus_ph(distSys, bus)
    ang = __get_ang_vanish(list_ph, v_pu_ang_dss)
    return ang
