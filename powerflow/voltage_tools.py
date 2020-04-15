import pandas as pd
from .systemclass import SystemClass
from .decorators import pf_tools

from .tools import __verify_bus_list, __get_bus_ang
from .tools import __get_bus_v_pu, __get_bus_ph
from .formatters import __identify_ph_config


@pf_tools
def get_all_v_pu_ang(distSys: SystemClass):
    buses = distSys.get_all_bus_names()
    return get_bus_v_pu_ang(distSys, buses)


@pf_tools
def get_bus_v_pu_ang(distSys: SystemClass, buses: list):
    list_verify = __verify_bus_list(distSys, buses)
    if not all(list_verify):
        for (verify, bus) in zip(list_verify, buses):
            if not verify:
                raise Exception(
                    f"A barra {bus} não está declarada no sistema")

    v_pu_list = []
    ang_list = []
    ph_list = []

    for bus in buses:
        ang_list.append(__get_bus_ang(distSys, bus))
        v_pu_list.append(__get_bus_v_pu(distSys, bus))
        ph = __get_bus_ph(distSys, bus)
        ph_config = __identify_ph_config(ph)
        ph_list.append(ph_config)

    df_bus_names = pd.DataFrame(buses, columns=['bus_names'])
    df_v_pu = pd.DataFrame(v_pu_list, columns=[
        'v_pu_a', 'v_pu_b', 'v_pu_c'])
    df_ang = pd.DataFrame(ang_list, columns=['ang_a', 'ang_b', 'ang_c'])
    df_ph = pd.DataFrame(ph_list, columns=['phases'])

    result = pd.concat(
        [df_bus_names, df_v_pu, df_ang, df_ph], axis=1, sort=False)
    return result
