from .systemclass import SystemClass
from .decorators import pf_tools
from .formatters import __check_elements
import pandas
from typing import List, Tuple
from operator import add


@pf_tools
def get_all_taps_number(distSys: SystemClass) -> pandas.DataFrame:
    """Gera o valor do tap para todos os reguladores.

    Arguments:
        distSys {powerflow.systemclass.SystemClass} -- Instância de SystemClass

    Returns:
        pandas.DataFrame -- Valor do tap para todos os reguladores
    """
    return get_tap_number(distSys, distSys.dss.RegControls.AllNames())


@pf_tools
def get_tap_number(
    distSys: SystemClass, reg_names: List[str]
) -> pandas.DataFrame:
    """Gera o valor do tap para os reguladores requisitados.

    Arguments:
        distSys {powerflow.systemclass.SystemClass} -- Instância de SystemClass
        reg_names {List[str]} -- Nome dos reguladores requisitados

    Returns:
        pandas.DataFrame -- Valor do tap para os reguladores requisitados.
    """

    def get_one(reg_name: str) -> Tuple[str, int]:
        distSys.dss.RegControls.Name(reg_name)
        return (reg_name, int(distSys.dss.RegControls.TapNumber()))

    __check_elements(reg_names, distSys.get_all_regs_names())

    return pandas.DataFrame(
        data=tuple(map(get_one, reg_names)), columns=["reg_name", "tap"]
    )


def get_taps_changes(tapDataFrame: pandas.DataFrame) -> pandas.DataFrame:
    """Conta a quantidade de mudança de taps ocorreram.

    Arguments:
        tapDataFrame {pandas.DataFrame} -- Retorno no modo timeseries da função
        powerflow.reg_tools.get_tap_number.

    Returns:
        pandas.DataFrame -- Valor da contagem de mudança dos taps.
    """

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
