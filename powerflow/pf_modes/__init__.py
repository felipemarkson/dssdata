import pandas as pd
from functools import reduce
from .. import SystemClass
from ..decorators import pf_tools


@pf_tools
def run_static_pf(distSys: SystemClass) -> None:
    distSys.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()


@pf_tools
def cfg_tspf(
    distSys: SystemClass, step_size: str = "1h", initial_time: tuple = (0, 0)
) -> None:

    cmd = f"set mode=daily stepsize={step_size} "
    cmd2 = f'time = "{initial_time[0]}, {initial_time[1]}"'
    distSys.run_command(cmd + cmd2)


@pf_tools
def __run_onestep_tspf(distSys: SystemClass) -> None:
    distSys.dss.Solution.Number(1)
    distSys.dss.Solution.Solve()


@pf_tools
def build_dataset_tspf(
    distSys: SystemClass,
    *,
    funcs_list: list = [lambda distSys: pd.Dataframe()],
    num_steps: int,
) -> tuple:
    def concat_dfs(list1, list2):
        df_lists = map(
            lambda df1, df2: pd.concat([df1, df2], ignore_index=True),
            list1,
            list2,
        )
        return df_lists

    def df_each_step(distSys: SystemClass, funcs_list, step):
        def run_funcs(distSys: SystemClass, func: callable, step: int):
            df = func(distSys)
            df["step"] = step
            return df

        __run_onestep_tspf(distSys)

        return tuple(
            map(lambda func: run_funcs(distSys, func, step), funcs_list)
        )

    all_steps_df = map(
        lambda step: df_each_step(distSys, funcs_list, step),
        range(0, num_steps),
    )

    data_list = reduce(concat_dfs, all_steps_df)

    return tuple(data_list)
