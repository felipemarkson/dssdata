import pandas
from functools import reduce
from .. import SystemClass
from ..decorators import pf_tools
from typing import Iterable, Tuple


@pf_tools
def run_static_pf(distSys: SystemClass) -> None:
    """
    Run the static power flow mode.

    Args:
        distSys: An instance of [SystemClass][dssdata.SystemClass]
    """
    distSys.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()


@pf_tools
def cfg_tspf(
    distSys: SystemClass, step_size: str = "1h", initial_time: tuple = (0, 0)
) -> None:
    """
    Set the time series mode in the distribution system.

    Args:
        distSys: An instance of [SystemClass][dssdata.SystemClass]
        step_size: The size of step time. See "Stepsize" in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf).
        initial_time:  See "Time" in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf).
    """  # noqa

    cmd = f"set mode=daily stepsize={step_size} "
    cmd2 = f'time = "{initial_time[0]}, {initial_time[1]}"'
    distSys.run_command(cmd + cmd2)


@pf_tools
def build_dataset_tspf(
    distSys: SystemClass, *, funcs_list: Iterable[callable], num_steps: int,
) -> Tuple[pandas.DataFrame]:
    """
    Build the datas of tools functions returns on time series mode. See [The main concept](../gettingstart/ideas.md).

    Args:
        distSys: An instance of [SystemClass][dssdata.SystemClass]
        funcs_list: Tools functions.
        num_steps : Number of time steps.

    Returns:
        [type]: Tools functions returns
    """  # noqa

    def __run_onestep_tspf(distSys: SystemClass) -> None:
        distSys.dss.Solution.Number(1)
        distSys.dss.Solution.Solve()

    def concat_dfs(list1, list2):
        df_lists = map(
            lambda df1, df2: pandas.concat([df1, df2], ignore_index=True),
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
