import pandas
from typing import List
from operator import add


def get_taps_changes(tapDataFrame: pandas.DataFrame) -> pandas.DataFrame:
    """
    Count the taps changes. That function is a reduction function.

    Args:
        tapDataFrame: The return of [get_all_taps_number][dssdata.tools.regs.get_all_taps_number] or [get_tap_number][dssdata.tools.regs.get_tap_number].

    Returns:
        The number of taps changes after time series power flow.
    """  # noqa

    def calc_one_step_chgs(first: list, second: list):
        return map(lambda data1, data2: abs(data1 - data2), first, second)

    def sum_changes_taps(list_df: List[list]):
        first = list_df[0]
        second = list_df[1]
        if len(list_df) == 2:
            return calc_one_step_chgs(first, second)
        else:
            return map(
                add,
                calc_one_step_chgs(first, second),
                sum_changes_taps(list_df[1:]),
            )

    iter_by_step = tapDataFrame.groupby(["step"])

    list_df = tuple(map(lambda data: data[1]["tap"].to_list(), iter_by_step))
    reg_names = tuple(
        map(lambda data: data[1]["reg_name"].to_list(), iter_by_step)
    )[0]

    return pandas.DataFrame(
        data=tuple(zip(reg_names, sum_changes_taps(list_df))),
        columns=["reg_name", "number_changes_tap"],
    )
