"""
Execute este codigo, apenas se você tiver certeza que
as funções estão corretas.
"""

# Static Series
# from powerflow.systemclass import SystemClass
# from powerflow.pf_modes import run_power_flow
# from powerflow.line_tools import get_all_line_infos
# from powerflow.voltage_tools import get_all_v_pu_ang
# from powerflow.pf_modes import cfg_tspf, buil_dataset_tspf
# from powerflow.reg_tools import get_all_taps_number
# import pandas as pd

# path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
# value_of_kV = [115, 4.16, 0.48]
# value_of_load_mult = 1


# distSys = SystemClass(
#     path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
# )


# reg_names = distSys.get_all_regs_names()
# bus_names = distSys.get_all_bus_names()
# line_names = distSys.get_all_lines_names()

# pd.DataFrame(data=reg_names, columns=["reg_name"]).to_json("reg_names.json")
# pd.DataFrame(data=bus_names, columns=["bus_name"]).to_json("bus_names.json")
# pd.DataFrame(
#     data=line_names,
#     columns=["line_name"]).to_json("line_names.json")
# run_power_flow(distSys)

# dataSet_vpu = get_all_v_pu_ang(distSys)
# dataSet_lines = get_all_line_infos(distSys)
# dataSet_taps = get_all_taps_number(distSys)
# dataSet_lines.to_json("all_line_infos.json")
# dataSet_vpu.to_json("all_v_pu_ang.json")
# dataSet_taps.to_json("taps_number.json")

# # Time Series
# path_of_system = "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"
# value_of_kV = [115, 4.16, 0.48]
# value_of_load_mult = 1


# distSys = SystemClass(
#     path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
# )

# cfg_tspf(distSys, "5m")

# [v_pu, line_infos] = buil_dataset_tspf(
#     distSys, funcs_list=[get_all_v_pu_ang, get_all_line_infos], num_steps=288
# )


# v_pu.to_json("v_pu_ang_all_13busTS.json")
# line_infos.to_json("line_infos_all_13busTS.json")
