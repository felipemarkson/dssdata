import pandas as pd
from ... import SystemClass
from ..._formatters import __check_elements


def __build_pd_dicts(
    distSys: SystemClass, element_name: str, element_type: str
) -> dict:

    distSys.dss.PDElements.Name(str(element_type) + "." + str(element_name))
    typ = distSys.dss.CktElement.Name().replace("." + str(element_name), "")

    losses = distSys.dss.CktElement.Losses()

    return {
        "type": typ,
        "name": element_name,
        "kw_losses": losses[0] / 1000,
        "kvar_losses": losses[1] / 1000,
    }


def pd_element_loss(
    distSys: SystemClass, element_name: str, element_type: str
) -> pd.DataFrame:
    """
    Get PD Element loss. 
    Ex:
        
    |   |     type    | name |     kw_losses     |    kvar_losses    |
    |:-:|:-----------:|:----:|:-----------------:|:-----------------:|
    | 0 | Transformer | xfm1 | 5.552671994055243 | 10.09627035828575 |

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]
        element_name: The name of the desired PD element
        element_type: The type of the PD element (Line or Transformer)

    Returns:
        A DataFrame containing the losses of the desired PD element.
    """  # noqa

    __check_elements(
        list((str(element_type) + "." + str(element_name)).split()),
        distSys.dss.Circuit.AllElementNames(),
    )
    pd_loss = []
    pd_loss.append(__build_pd_dicts(distSys, element_name, element_type))
    return pd.DataFrame(pd_loss)


def pd_element_loss_list(
    distSys: SystemClass, element_names: list, element_type: str
) -> pd.DataFrame:
    """
    Get PD Element loss List. 
    Ex:
        
    |   |     type    | name |      kw_losses      |     kvar_losses     |
    |:-:|:-----------:|:----:|:-------------------:|:-------------------:|
    | 0 | Transformer |  sub | 0.03228776756674051 | 0.26246840671868993 |
    | 1 | Transformer | reg1 | 0.12209426402417012 | 0.12385869008488953 |
    | 2 | Transformer | reg2 | 0.06534502545557916 | 0.06707698704162612 |
    | 3 | Transformer | reg3 |  0.1350894299906213 | 0.13685391995031387 |
    | 4 | Transformer | xfm1 |  5.552671994055243  |  10.09627035828575  |


    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]
        element_names: A list of names of the desired PD elements
        element_type: The type of the PD elements (Line or Transformer)

    Returns:
        A DataFrame containing the losses of the desired list of PD elements.
    """  # noqa

    if element_type == "Line":
        __check_elements(element_names, distSys.dss.Lines.AllNames())
    elif element_type == "Transformer":
        __check_elements(element_names, distSys.dss.Transformers.AllNames())

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ),
                element_names,
            )
        )
    )


def get_all_line_losses(distSys: SystemClass) -> pd.DataFrame:
    """
    Get all lines losses. 
    Ex:
        
    |    | type |  name  |       kw_losses       |       kvar_losses      |
    |:--:|:----:|:------:|:---------------------:|:----------------------:|
    |  0 | Line | 650632 |   60.73738438443188   |   196.01456922721653   |
    |  1 | Line | 632670 |   12.990633124585496  |    41.49451118066639   |
    |  2 | Line | 670671 |   22.728758590972518  |    72.33414340631373   |
    |  3 | Line | 671680 | 8.613828479544935e-12 |  -0.004169229516017848 |
    |  4 | Line | 632633 |   0.8244871671261499  |   1.0561418323197722   |
    |  5 | Line | 632645 |    2.75857850181032   |   2.4159107795492454   |
    |  6 | Line | 645646 |   0.5274715389783668  |   0.41973513183818434  |
    |  7 | Line | 692675 |   4.1629544212549225  |    2.419339661740261   |
    |  8 | Line | 671684 |   0.5794876384501113  |   0.47068061342113654  |
    |  9 | Line | 684611 |   0.3824044250881998  |   0.38734916932047053  |
    | 10 | Line | 684652 |   0.7998267312559038  |    0.230879175578375   |
    | 11 | Line | 671692 | 9.054614813067019e-06 | 4.3655745685100556e-14 |

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]

    Returns:
        A DataFrame containing all line losses.
    """  # noqa

    element_type = "Line"

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ),
                distSys.dss.Lines.AllNames(),
            )
        )
    )


def get_all_transformers_losses(distSys: SystemClass) -> pd.DataFrame:
    """
    Get all transformers losses. 
    Ex:
        
    |   |     type    | name |      kw_losses      |     kvar_losses     |
    |:-:|:-----------:|:----:|:-------------------:|:-------------------:|
    | 0 | Transformer |  sub | 0.03228776756674051 | 0.26246840671868993 |
    | 1 | Transformer | reg1 | 0.12209426402417012 | 0.12385869008488953 |
    | 2 | Transformer | reg2 | 0.06534502545557916 | 0.06707698704162612 |
    | 3 | Transformer | reg3 |  0.1350894299906213 | 0.13685391995031387 |
    | 4 | Transformer | xfm1 |  5.552671994055243  |  10.09627035828575  |

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]

    Returns:
        A DataFrame containing all transformers losses.
    """  # noqa

    element_type = "Transformer"

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ),
                distSys.dss.Transformers.AllNames(),
            )
        )
    )


def get_all_pd_elements_losses(distSys: SystemClass) -> pd.DataFrame:
    """
    Get all PD Elements losses. 
    Ex:
        
    |    |     type    |  name  |       kw_losses       |       kvar_losses      |
    |:--:|:-----------:|:------:|:---------------------:|:----------------------:|
    |  0 | Transformer |   sub  |  0.03228776756674051  |   0.26246840671868993  |
    |  1 | Transformer |  reg1  |  0.12209426402417012  |   0.12385869008488953  |
    |  2 | Transformer |  reg2  |  0.06534502545557916  |   0.06707698704162612  |
    |  3 | Transformer |  reg3  |   0.1350894299906213  |   0.13685391995031387  |
    |  4 | Transformer |  xfm1  |   5.552671994055243   |    10.09627035828575   |
    |  5 |     Line    | 650632 |   60.73738438443188   |   196.01456922721653   |
    |  6 |     Line    | 632670 |   12.990633124585496  |    41.49451118066639   |
    |  7 |     Line    | 670671 |   22.728758590972518  |    72.33414340631373   |
    |  8 |     Line    | 671680 | 8.613828479544935e-12 |  -0.004169229516017848 |
    |  9 |     Line    | 632633 |   0.8244871671261499  |   1.0561418323197722   |
    | 10 |     Line    | 632645 |    2.75857850181032   |   2.4159107795492454   |
    | 11 |     Line    | 645646 |   0.5274715389783668  |   0.41973513183818434  |
    | 12 |     Line    | 692675 |   4.1629544212549225  |    2.419339661740261   |
    | 13 |     Line    | 671684 |   0.5794876384501113  |   0.47068061342113654  |
    | 14 |     Line    | 684611 |   0.3824044250881998  |   0.38734916932047053  |
    | 15 |     Line    | 684652 |   0.7998267312559038  |    0.230879175578375   |
    | 16 |     Line    | 671692 | 9.054614813067019e-06 | 4.3655745685100556e-14 |

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]

    Returns:
        A DataFrame containing all PD Elements losses.
    """  # noqa

    line_losses = get_all_line_losses(distSys)

    transformer_losses = get_all_transformers_losses(distSys)

    return pd.concat([transformer_losses, line_losses])


def get_total_pd_elements_losses(distSys: SystemClass) -> pd.DataFrame:
    """
    Get Total PD Elements losses. 
    Ex:
        
    |   |       name      |   kw_losses_total  | kvar_losses_total |
    |:-:|:---------------:|:------------------:|:-----------------:|
    | 0 | all_pd_elements | 112.39948405966965 | 327.9256193105294 |

    Args:
        distSys: An instance of  [SystemClass][dssdata.SystemClass]

    Returns:
        A DataFrame containing the sum of losses of all PD Elements.
    """  # noqa

    data_loss = []
    data = {
        "name": "all_pd_elements",
        "kw_losses_total": sum(
            get_all_pd_elements_losses(distSys)["kw_losses"]
        ),
        "kvar_losses_total": sum(
            get_all_pd_elements_losses(distSys)["kvar_losses"]
        ),
    }

    data_loss.append(data)
    return pd.DataFrame(data_loss)
