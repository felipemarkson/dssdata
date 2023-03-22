import pandas


def get_taps_changes(tapDataFrame: pandas.DataFrame) -> pandas.DataFrame:
    """
    Count the taps changes. That function is a reduction function.

    E.g.:
    If a trafo starts in tap number 4 and goes to tap number -3.
    The result is 7. 
    
    `(4 -> 3 -> 2 -> 1 -> 0 -> -1 -> -2 -> -3)`

    Args:
        tapDataFrame: The return of [get_all_taps_number][dssdata.tools.regs.get_all_taps_number] or [get_tap_number][dssdata.tools.regs.get_tap_number].

    Returns:
        The number of taps changes after time series power flow.
    """  # noqa

    mapper = {"tap": "number_changes_tap"}

    def prepair_df(df, step):
        return df.loc[step].reset_index(drop=True).rename(columns=mapper)

    df = tapDataFrame.set_index(["step"])
    steps = df.index.unique()

    df_new = prepair_df(df, steps[0])
    df_new["number_changes_tap"] = 0

    df_prev = prepair_df(df, steps[0])

    for step in steps:
        df_step = prepair_df(df, step)
        diff = abs(df_prev["number_changes_tap"] - df_step["number_changes_tap"])
        df_new["number_changes_tap"] += diff
        df_prev = df_step

    return df_new
