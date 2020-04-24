import pandas as pd
from .systemclass import SystemClass
from .decorators import pf_tools

from .formatters import (
    __identify_ph_config,
    __get_mag_vanish,
    __get_ang_vanish,
    __remove_nones_from_lists,
)


@pf_tools
def get_line_infos(distSys: SystemClass, lines_names: list) -> pd.DataFrame:
    """
    TODO: Verificação se todos os items do line_names existe no sistema
    """
    def vanish_line_infos(bus_raw: list, current_raw: list) -> tuple:
        bus_name = bus_raw[0]
        phs_raw = list(map(lambda bus: int(bus), bus_raw[1:]))
        phs_data = phs_raw if phs_raw != [] else [1, 2, 3]
        phs = __identify_ph_config(phs_data)
        currents_mag = __get_mag_vanish(phs_data, current_raw)
        currents_ang = __get_ang_vanish(phs_data, current_raw)

        return (bus_name, phs, currents_mag, currents_ang)

    def build_line_dicts(distSys: SystemClass, line_name: str) -> dict:
        distSys.dss.Lines.Name(line_name)
        losses = distSys.dss.CktElement.Losses()
        normalAmps = distSys.dss.CktElement.NormalAmps()
        emergAmps = distSys.dss.CktElement.EmergAmps()
        currents_raw = distSys.dss.CktElement.CurrentsMagAng()
        currents_raw_bus1 = currents_raw[:int(len(currents_raw) / 2)]
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
        list(
            map(
                lambda line_name: build_line_dicts(distSys, line_name),
                lines_names,
            )
        )
    )


@pf_tools
def get_all_line_infos(distSys: SystemClass) -> pd.DataFrame:
    line_names = distSys.get_all_lines_names()
    return get_line_infos(distSys, line_names)
