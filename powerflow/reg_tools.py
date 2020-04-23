from .systemclass import SystemClass
from .decorators import pf_tools
from .formatters import __check_elements
import pandas
from typing import List, Tuple


@pf_tools
def get_all_taps_number(distSys: SystemClass) -> pandas.DataFrame:
    """Gera o valor do tap para todos os reguladores.

    Arguments:
        distSys {powerflow.systemclass.SystemClass} -- Instância de SystemClass

    Returns:
        pandas.DataFrame -- Valor do tap para todos os reguladores
    """
    return get_reg_tap_number(distSys, distSys.dss.RegControls.AllNames())


@pf_tools
def get_reg_tap_number(
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
        """Função auxiliar para map.

        Arguments:
            reg_name {str} -- Nome do regulador

        Returns:
            Tuple[str, int] -- (Nome do regulador, Número de tap)
        """

        distSys.dss.RegControls.Name(reg_name)

        return (reg_name, int(distSys.dss.RegControls.TapNumber()))

    __check_elements(reg_names, distSys.get_all_regs_names())

    return pandas.DataFrame(
        data=list(map(get_one, reg_names)), columns=["reg_name", "tap"]
    )


def __get_taps_changes(
    distSys: SystemClass, reg_names: List[str]
) -> pandas.DataFrame:
    """
    TODO: fazer o taps changes por step.
    """
    pass


def get_taps_changes(tapDataFrame: pandas.DataFrame) -> pandas.DataFrame:

    def changes_of_one_step(first: list, second: list) -> list:
        return map(lambda data1, data2: abs(data1 - data2), first, second)

    def sum_changes_taps(list_df: List[list]) -> list:
        first = list_df[0]
        second = list_df[1]
        if len(list_df) == 2:
            return changes_of_one_step(first, second)
        else:
            return list(
                map(
                    lambda data1, data2: data1 + data2,
                    changes_of_one_step(first, second),
                    sum_changes_taps(list_df[1:]),
                )
            )

    iter_by_step = tapDataFrame.groupby(["step"])

    list_df = list(map(lambda data: data[1]["tap"].to_list(), iter_by_step))
    reg_names = list(
        map(lambda data: data[1]["reg_name"].to_list(), iter_by_step)
    )[0]

    return pandas.DataFrame(
        data=list(
            map(
                lambda name, changes: (name, changes),
                reg_names,
                sum_changes_taps(list_df),
            )
        ),
        columns=["reg_name", "number_changes_tap"],
    )
