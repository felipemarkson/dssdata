import pandas as pd
from functools import reduce
from .voltage_tools import get_all_v_pu_ang, get_bus_v_pu_ang
from .systemclass import SystemClass


def run_power_flow(distSys: SystemClass):
    distSys.dss.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()


def cfg_tspf(distSys: SystemClass,
             step_size: str = '',
             initial_time: tuple = (0, 0)):

    distSys.dss.run_command(
        f'set mode=daily stepsize={step_size} time = "{initial_time[0]}, {initial_time[1]}"')


def run_onestep_tspf(distSys: SystemClass):
    distSys.dss.Solution.Number(1)
    distSys.dss.Solution.Solve()


def buil_dataset_tspf(distSys: SystemClass, funcs_list: list, num_steps: int):

    def run_funcs(func, step):
        df = func(distSys)
        df['step'] = step
        return df

    def concat(list1, list2):
        df_lists = map(lambda df1, df2: pd.concat(
            [df1, df2], ignore_index=True), list1, list2)
        return df_lists

    def df_each_step(step):
        run_onestep_tspf(distSys)
        df_lists_step = list(
            map(lambda func: run_funcs(func, step), funcs_list))
        return df_lists_step

    all_steps_df = map(df_each_step, range(0, num_steps))

    data_list = reduce(concat, all_steps_df)

    return list(data_list)
