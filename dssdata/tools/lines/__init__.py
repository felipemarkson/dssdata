import pandas as pd
from ... import SystemClass
from ...decorators import tools

from ..._formatters import (
    __identify_ph_config,
    __get_mag_vanish,
    __get_ang_vanish,
    __remove_nones_from_lists,
    __check_elements,
)

from typing import List


@tools
def get_infos(distSys: SystemClass, names: List[str]) -> pd.DataFrame:
    """
    Get some relevant infos from lines.
    Ex:

    |    | name   | bus1 | ph_bus1 | bus2 | ph_bus2 | I(A)_bus1_ph_a | I(A)_bus1_ph_b | I(A)_bus1_ph_c | I(A)_bus2_ph_a | I(A)_bus2_ph_b | I(A)_bus2_ph_c | ang_bus1_ph_a | ang_bus1_ph_b | ang_bus1_ph_c | ang_bus2_ph_a | ang_bus2_ph_b | ang_bus2_ph_c | kw_losses | kvar_losses | emergAmps | normAmps | perc_NormAmps | perc_EmergAmps |
    |----|--------|------|---------|------|---------|----------------|----------------|----------------|----------------|----------------|----------------|---------------|---------------|---------------|---------------|---------------|---------------|-----------|-------------|-----------|----------|---------------|----------------|
    | 0  | 650632 | rg60 | abc     | 632  | abc     | 562.609        | 419.029        | 591.793        | 562.61         | 419.03         | 591.794        | -28.7         | -141.3        | 93.4          | 151.3         | 38.7          | -86.6         | 60.737    | 196.015     | 600.0     | 400.0    | 1.479         | 0.986          |
    | 1  | 632670 | 632  | abc     | 670  | abc     | 481.916        | 218.055        | 480.313        | 481.916        | 218.055        | 480.313        | -27.2         | -135.2        | 99.6          | 152.8         | 44.8          | -80.4         | 12.991    | 41.495      | 600.0     | 400.0    | 1.205         | 0.803          |
    | 2  | 670671 | 670  | abc     | 671  | abc     | 473.795        | 188.824        | 424.942        | 473.795        | 188.824        | 424.942        | -27.0         | -132.6        | 101.3         | 153.0         | 47.4          | -78.7         | 22.729    | 72.334      | 600.0     | 400.0    | 1.184         | 0.79           |

    Args:
        distSys : An instance of [SystemClass][dssdata.SystemClass].
        names : Lines names.

    Returns:
        Lines infos.
    """  # noqa

    __check_elements(names, distSys.dss.Lines.AllNames())

    def build_line_dicts(distSys: SystemClass, line_name: str) -> dict:
        def vanish_line_infos(bus_raw: list, current_raw: list) -> tuple:
            bus_name = bus_raw[0]
            phs_raw = list(map(lambda bus: int(bus), bus_raw[1:]))
            phs_data = phs_raw if phs_raw != [] else [1, 2, 3]
            phs = __identify_ph_config(phs_data)
            currents_mag = __get_mag_vanish(phs_data, current_raw)
            currents_ang = __get_ang_vanish(phs_data, current_raw)

            return (bus_name, phs, currents_mag, currents_ang)

        distSys.dss.Lines.Name(line_name)
        losses = distSys.dss.CktElement.Losses()
        normalAmps = distSys.dss.CktElement.NormalAmps()
        emergAmps = distSys.dss.CktElement.EmergAmps()
        currents_raw = distSys.dss.CktElement.CurrentsMagAng()
        currents_raw_bus1 = currents_raw[: int(len(currents_raw) / 2)]
        currents_raw_bus2 = currents_raw[int(len(currents_raw) / 2):]

        bus_raw = distSys.dss.Lines.Bus1().split(".")

        (bus_name1, phs1, currents_mag1, currents_ang1) = vanish_line_infos(
            bus_raw, currents_raw_bus1
        )
        bus_raw = distSys.dss.Lines.Bus2().split(".")
        (bus_name2, phs2, currents_mag2, currents_ang2) = vanish_line_infos(
            bus_raw, currents_raw_bus2
        )

        currents_mag1_calc = __remove_nones_from_lists(currents_mag1)
        currents_mag2_calc = __remove_nones_from_lists(currents_mag2)

        return {
            "name": line_name,
            "bus1": bus_name1,
            "ph_bus1": phs1,
            "bus2": bus_name2,
            "ph_bus2": phs2,
            "I(A)_bus1_ph_a": currents_mag1[0],
            "I(A)_bus1_ph_b": currents_mag1[1],
            "I(A)_bus1_ph_c": currents_mag1[2],
            "I(A)_bus2_ph_a": currents_mag2[0],
            "I(A)_bus2_ph_b": currents_mag2[1],
            "I(A)_bus2_ph_c": currents_mag2[2],
            "ang_bus1_ph_a": currents_ang1[0],
            "ang_bus1_ph_b": currents_ang1[1],
            "ang_bus1_ph_c": currents_ang1[2],
            "ang_bus2_ph_a": currents_ang2[0],
            "ang_bus2_ph_b": currents_ang2[1],
            "ang_bus2_ph_c": currents_ang2[2],
            "kw_losses": losses[0] / 1000,
            "kvar_losses": losses[1] / 1000,
            "emergAmps": emergAmps,
            "normAmps": normalAmps,
            "perc_NormAmps": max(currents_mag1_calc + currents_mag2_calc)
            / normalAmps,
            "perc_EmergAmps": max(currents_mag1_calc + currents_mag2_calc)
            / emergAmps,
        }

    return pd.DataFrame(
        tuple(
            map(lambda line_name: build_line_dicts(distSys, line_name), names,)
        )
    )


@tools
def get_all_infos(distSys: SystemClass) -> pd.DataFrame:
    """
    Get some relevant infos from all lines. See [get_infos][dssdata.tools.lines.get_infos].

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]

    Returns:
        All lines infos
    """  # noqa
    line_names = distSys.dss.Lines.AllNames()
    return get_infos(distSys, line_names)
