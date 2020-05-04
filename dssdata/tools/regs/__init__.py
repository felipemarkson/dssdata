from ... import SystemClass
from ...decorators import pf_tools
from ..._formatters import __check_elements
import pandas
from typing import List, Tuple


@pf_tools
def get_all_taps_number(distSys: SystemClass) -> pandas.DataFrame:
    """
    Get the tap number of all regulators.

    Args:
        distSys:  An instance of  [SystemClass][dssdata.SystemClass].
    Returns:
        The tap number of all regulators.
    """
    return get_tap_number(distSys, distSys.dss.RegControls.AllNames())


@pf_tools
def get_tap_number(
    distSys: SystemClass, names: List[str]
) -> pandas.DataFrame:
    """
    Get the tap number of regulators.

    Args:
        distSys : An instance of  [SystemClass][dssdata.SystemClass].
        names : Regulators names

    Returns:
        The tap number of regulators.
    """

    def get_one(reg_name: str) -> Tuple[str, int]:
        distSys.dss.RegControls.Name(reg_name)
        return (reg_name, int(distSys.dss.RegControls.TapNumber()))

    __check_elements(names, distSys.get_all_regs_names())

    return pandas.DataFrame(
        data=tuple(map(get_one, names)), columns=["reg_name", "tap"]
    )
