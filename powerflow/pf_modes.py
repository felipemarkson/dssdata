import pandas as pd
from functools import reduce
from .systemclass import SystemClass
from .decorators import pf_tools


@pf_tools
def run_power_flow(distSys: SystemClass):
    distSys.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()


@pf_tools
def cfg_tspf(
    distSys: SystemClass, step_size: str = "1h", initial_time: tuple = (0, 0)
):

    cmd = f"set mode=daily stepsize={step_size} "
    cmd2 = f'time = "{initial_time[0]}, {initial_time[1]}"'
    distSys.run_command(cmd + cmd2)


@pf_tools
def __run_onestep_tspf(distSys: SystemClass):
    distSys.dss.Solution.Number(1)
    distSys.dss.Solution.Solve()


@pf_tools
def buil_dataset_tspf(
    distSys: SystemClass,
    *,
    funcs_list: list = [lambda distSys: pd.Dataframe()],
    num_steps: int,
) -> list:
    def concat_dfs(list1, list2):
        df_lists = map(
            lambda df1, df2: pd.concat([df1, df2], ignore_index=True),
            list1,
            list2,
        )
        return df_lists

    @pf_tools
    def df_each_step(distSys: SystemClass, funcs_list, step):
        def run_funcs(distSys: SystemClass, func: callable, step: int):
            df = func(distSys)
            df["step"] = step
            return df

        __run_onestep_tspf(distSys)

        return list(
            map(lambda func: run_funcs(distSys, func, step), funcs_list)
        )

    all_steps_df = map(
        lambda step: df_each_step(distSys, funcs_list, step),
        range(0, num_steps),
    )

    data_list = reduce(concat_dfs, all_steps_df)

    return list(data_list)
