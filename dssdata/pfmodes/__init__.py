import pandas
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

    def runmode_one_step(distSys):
        distSys.dss.Solution.Number(1)
        distSys.dss.Solution.Solve()

    def run_tool(distSys, tool, step):
        df = tool(distSys)
        df["step"] = step
        return df

    def run_concepts(distSys, actions, tools, step):
        for action in actions:
            action(distSys)

        runmode_one_step(distSys)

        return [run_tool(distSys, tool, step) for tool in tools]

    def all_steps_tool(all_steps_result, steps, indx_tool):
        return pandas.concat(
            [all_steps_result[step][indx_tool] for step in steps],
            ignore_index=True,
        )

    steps = range(0, num_steps)

    all_steps_result = [
        run_concepts(distSys, actions, tools, step) for step in steps
    ]

    return [
        all_steps_tool(all_steps_result, steps, indx)
        for indx, _ in enumerate(tools)
    ]
