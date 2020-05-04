import pandas
from ... import SystemClass
from ...decorators import pf_tools

from ..._tools import __get_bus_v_pu, __get_bus_ph, __get_bus_ang
from ..._formatters import __identify_ph_config, __check_elements
from typing import List


@pf_tools
def get_all(distSys: SystemClass) -> pandas.DataFrame:
    """
    Get line to neutral voltages (module and angle) in p.u. and phases configuration from buses. See [get_from_buses][dssdata.tools.voltages.get_from_buses].

    Args:
        distSys : An instance of  [SystemClass][dssdata.SystemClass].

    Returns:
        [type]: Line to neutral voltages (module and angle) in p.u. and phases configuration from buses. 
    """  # noqa

    buses = distSys.get_all_bus_names()
    return get_from_buses(distSys, buses)


@pf_tools
def get_from_buses(distSys: SystemClass, buses: List[str]) -> pandas.DataFrame:
    """

    Get line to neutral voltages (module and angle) in p.u. and phases configuration from buses. 

    |    | bus_name | v_pu_a  | v_pu_b  | v_pu_c  | ang_a | ang_b  | ang_c | phases |
    |----|-----------|---------|---------|---------|-------|--------|-------|--------|
    | 0  | sourcebus | 0.99997 | 0.99999 | 0.99995 | 30.0  | -90.0  | 150.0 | abc    |
    | 1  | 646       |   NaN      | 1.01803 | 1.00026 |   NaN    | -122.0 | 117.8 | bc     |
    | 2 | 611       |    NaN     |    NaN     | 0.96083 |   NaN    |    NaN    | 115.7 | c      |
    | 3 | 652       | 0.97533 |    NaN     |   NaN      | -5.3  |    NaN    |  NaN     | a      |


    Args:
        distSys : An instance of  [SystemClass][dssdata.SystemClass].
        buses : Buses names.

    Returns:
        [type]: Line to neutral voltages (module and angle) in p.u. and phases configuration from buses. 
    """  # noqa

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

    df_bus_names = pandas.DataFrame(buses, columns=["bus_name"])
    df_v_pu = pandas.DataFrame(
        v_pu_list, columns=["v_pu_a", "v_pu_b", "v_pu_c"]
    )
    df_ang = pandas.DataFrame(ang_list, columns=["ang_a", "ang_b", "ang_c"])
    df_ph = pandas.DataFrame(ph_list, columns=["phase"])

    result = pandas.concat(
        (df_bus_names, df_v_pu, df_ang, df_ph), axis=1, sort=False
    )
    return result
