import pandas
from functools import reduce
from .. import SystemClass
from ..decorators import actions, mode
from typing import Iterable, Tuple, Callable


@mode
def run_static_pf(
    distSys: SystemClass,
    actions: Iterable[Callable] = (lambda distSys: None,),
    tools: Iterable[Callable] = (lambda distSys: None,),
) -> tuple:
    """
    Run the static power flow mode.
    To see how it works, see [Learning DSSData](../tutorial/#static-power-flow).

    Args:
        distSys: An instance of [SystemClass][dssdata.SystemClass]
        actions: Actions functions.
        tools: Tools functions.

    Returns:
        Tools functions returns
    """  # noqa
    [action(distSys) for action in actions]
    distSys.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()
    return tuple(tool(distSys) for tool in tools)


@actions
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


@mode
def run_tspf(
    distSys: SystemClass,
    num_steps: int,
    actions: Iterable[Callable] = (lambda distSys: None,),
    tools: Iterable[Callable] = (lambda distSys: None,),
) -> Tuple[pandas.DataFrame]:
    """
    Run the time series power flow.
    To see how it works, see [Learning DSSData](../tutorial/#time-series-power-flow).

    Args:
        distSys: An instance of [SystemClass][dssdata.SystemClass]
        num_steps : Number of time steps.
        actions: Actions functions.
        tools: Tools functions.
        

    Returns:
        Tools functions returns for all steps
    """  # noqa

    def concat_dfs(list_df1, list_df2):
        """
        Concatena dois conjuntos de DF par a par. Ex:
        list_df1 = [df1, df2, df3]
        list_df2 = [df4, df5, df6]
        return [pd.concat(df1,df4), pd.concat(df2,df5), pd.concat(df3,df6)]

        Args:
            list_df1 ([type]): [description]
            list_df2 ([type]): [description]

        Returns:
            [type]: [description]
        """
        return map(
            lambda df1, df2: pandas.concat([df1, df2], ignore_index=True),
            list_df1,
            list_df2,
        )

    def runmode_one_step(distSys):
        distSys.dss.Solution.Number(1)
        distSys.dss.Solution.Solve()

    def run_tool(distSys, tool, step):
        df = tool(distSys)
        df["step"] = step
        return df

    def run_concetps(distSys, step):
        [action(distSys) for action in actions]
        runmode_one_step(distSys)
        return tuple(run_tool(distSys, tool, step) for tool in tools)

    all_steps = (run_concetps(distSys, step) for step in range(0, num_steps))

    return tuple(reduce(concat_dfs, all_steps))
