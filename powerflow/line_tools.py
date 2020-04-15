import pandas as pd
from .systemclass import SystemClass
from .decorators import pf_tools

from .formatters import (
    __identify_ph_config,
    __get_mag_vanish,
    __get_ang_vanish)


@pf_tools
def get_line_infos(distSys: SystemClass, lines_names: list):

    def vanish_line_infos(bus_raw: list, current_raw: list):
        bus_name = bus_raw[0]
        phs_raw = list(map(lambda bus: int(bus), bus_raw[1:]))
        if phs_raw == []:
            phs_raw = [1, 2, 3]
        phs = __identify_ph_config(phs_raw)
        currents_mag = __get_mag_vanish(phs_raw, current_raw)
        currents_ang = __get_ang_vanish(phs_raw, current_raw)

        return (bus_name, phs, currents_mag, currents_ang)

    data_list = []

    for line_name in lines_names:
        distSys.dss.Lines.Name(line_name)
        losses = distSys.dss.CktElement.Losses()
        normalAmps = distSys.dss.CktElement.NormalAmps()
        emergAmps = distSys.dss.CktElement.EmergAmps()
        currents_raw = distSys.dss.CktElement.CurrentsMagAng()
        currents_raw_bus1 = currents_raw[:int(len(currents_raw)/2)]
        currents_raw_bus2 = currents_raw[int(len(currents_raw)/2):]

        bus_raw = distSys.dss.Lines.Bus1().split('.')
        (bus_name1, phs1,
            currents_mag1, currents_ang1) = vanish_line_infos(
            bus_raw, currents_raw_bus1)
        bus_raw = distSys.dss.Lines.Bus2().split('.')
        (bus_name2, phs2,
            currents_mag2, currents_ang2) = vanish_line_infos(
            bus_raw, currents_raw_bus2)

        currents_mag1_calc = currents_mag1.copy()
        while None in currents_mag1_calc:
            currents_mag1_calc.remove(None)
        currents_mag2_calc = currents_mag2.copy()
        while None in currents_mag2_calc:
            currents_mag2_calc.remove(None)

        data = {
            'name': line_name,
            'bus1': bus_name1,
            'ph_bus1': phs1,
            'bus2': bus_name2,
            'ph_bus2': phs2,
            'I(A)_bus1_ph_a': round(currents_mag1[0], 3)
            if currents_mag1[0] is not None else None,
            'I(A)_bus1_ph_b': round(currents_mag1[1], 3)
            if currents_mag1[1] is not None else None,
            'I(A)_bus1_ph_c': round(currents_mag1[2], 3)
            if currents_mag1[2] is not None else None,
            'I(A)_bus2_ph_a': round(currents_mag2[0], 3)
            if currents_mag2[0] is not None else None,
            'I(A)_bus2_ph_b': round(currents_mag2[1], 3)
            if currents_mag2[1] is not None else None,
            'I(A)_bus2_ph_c': round(currents_mag2[2], 3)
            if currents_mag2[2] is not None else None,
            'ang_bus1_ph_a': round(currents_ang1[0], 2)
            if currents_ang1[0] is not None else None,
            'ang_bus1_ph_b': round(currents_ang1[1], 2)
            if currents_ang1[1] is not None else None,
            'ang_bus1_ph_c': round(currents_ang1[2], 2)
            if currents_ang1[2] is not None else None,
            'ang_bus2_ph_a': round(currents_ang2[0], 2)
            if currents_ang2[0] is not None else None,
            'ang_bus2_ph_b': round(currents_ang2[1], 2)
            if currents_ang2[1] is not None else None,
            'ang_bus2_ph_c': round(currents_ang2[2], 2)
            if currents_ang2[2] is not None else None,
            'kw_losses': round(losses[0]/1000, 3),
            'kvar_losses': round(losses[1]/1000, 3),
            'emergAmps': round(emergAmps, 3),
            'normAmps': round(normalAmps, 3),
            'perc_NormAmps': round(
                max(
                    currents_mag1_calc + currents_mag2_calc)/normalAmps, 3
            ),
            'perc_EmergAmps': round(
                max(
                    currents_mag1_calc + currents_mag2_calc)/emergAmps, 3
            ),
        }
        data_list.append(data)

    return pd.DataFrame(data_list)


@pf_tools
def get_all_line_infos(distSys: SystemClass):
    line_names = distSys.get_all_lines_names()
    return get_line_infos(distSys, line_names)
