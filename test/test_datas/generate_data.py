"""
Execute este codigo, apenas se você tiver certeza que
as funções estão corretas.
"""


from powerflow.systemclass import SystemClass
from powerflow.pf_modes import run_power_flow
from powerflow.line_tools import get_all_line_infos
from powerflow.voltage_tools import get_all_v_pu_ang
from powerflow.pf_modes import cfg_tspf, buil_dataset_tspf

path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
value_of_kV = [115, 4.16, 0.48]
value_of_load_mult = 1


distSys = SystemClass(
    path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
)

run_power_flow(distSys)

dataSet_vpu = get_all_v_pu_ang(distSys)
dataSet_lines = get_all_line_infos(distSys)
dataSet_lines.to_json("all_line_infos.json")
dataSet_vpu.to_json("all_v_pu_ang.json")


path_of_system = "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"
value_of_kV = [115, 4.16, 0.48]
value_of_load_mult = 1


distSys = SystemClass(
    path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
)

cfg_tspf(distSys, "5m")

[v_pu, line_infos] = buil_dataset_tspf(
    distSys, funcs_list=[get_all_v_pu_ang, get_all_line_infos], num_steps=288
)


v_pu.to_json("v_pu_ang_all_13busTS.json")
line_infos.to_json("line_infos_all_13busTS.json")
