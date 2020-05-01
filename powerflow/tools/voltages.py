import pandas as pd
from .. import SystemClass
from ..decorators import pf_tools

from .._tools import __get_bus_v_pu, __get_bus_ph, __get_bus_ang
from .._formatters import __identify_ph_config, __check_elements


@pf_tools
def get_all(distSys: SystemClass):
    buses = distSys.get_all_bus_names()
    return get_from_buses(distSys, buses)


@pf_tools
def get_from_buses(distSys: SystemClass, buses: list) -> pd.DataFrame:
    __check_elements(buses, distSys.get_all_bus_names())

    def agreggate(bus: str):
        return (
            __get_bus_ang(distSys, bus),
            __get_bus_v_pu(distSys, bus),
            __identify_ph_config(__get_bus_ph(distSys, bus)),
        )

    (ang_list, v_pu_list, ph_list) = tuple(
        zip(*(agreggate(bus) for bus in buses))
    )

    df_bus_names = pd.DataFrame(buses, columns=["bus_name"])
    df_v_pu = pd.DataFrame(v_pu_list, columns=["v_pu_a", "v_pu_b", "v_pu_c"])
    df_ang = pd.DataFrame(ang_list, columns=["ang_a", "ang_b", "ang_c"])
    df_ph = pd.DataFrame(ph_list, columns=["phase"])

    result = pd.concat(
        (df_bus_names, df_v_pu, df_ang, df_ph), axis=1, sort=False
    )
    return result
