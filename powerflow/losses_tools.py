import pandas as pd
from .systemclass import SystemClass
from .formatters import __check_elements



def __build_pd_dicts(
    distSys: SystemClass, element_name: str, element_type: str
) -> dict:

    distSys.dss.PDElements.Name(str(element_type)+'.'+str(element_name))
    typ = distSys.dss.CktElement.Name().replace("."+str(element_name), "")

    losses = distSys.dss.CktElement.Losses()

    return {
        'type': typ,
        'name': element_name,
        'kw_losses': losses[0] / 1000,
        'kvar_losses': losses[1] / 1000,
        }


def pd_element_loss(
    distSys: SystemClass, element_name: str, element_type: str
) -> pd.DataFrame:

    __check_elements(
        list(
            (str(element_type)+'.'+str(element_name)).split()
        ),
        distSys.dss.Circuit.AllElementNames()
    )
    pd_loss = []
    pd_loss.append(
        __build_pd_dicts(
            distSys, element_name, element_type
            )
    )
    return pd.DataFrame(pd_loss)


def pd_element_loss_list(
    distSys: SystemClass, element_names: list, element_type: str
) -> pd.DataFrame:

    if element_type == "List":
        __check_elements(
            element_names, distSys.dss.Lines.AllNames()
        )
    elif element_type == "Transformer":
        __check_elements(
            element_names, distSys.dss.Transformers.AllNames()
        )

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ), element_names
            )
        )
    )


def get_all_line_losses(distSys: SystemClass) -> pd.DataFrame:

    element_type = 'Line'

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ), distSys.dss.Lines.AllNames()
            )
        )
    )


def get_all_transformers_losses(distSys: SystemClass) -> pd.DataFrame:

    element_type = 'Transformer'

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: __build_pd_dicts(
                    distSys, element_name, element_type
                ), distSys.dss.Transformers.AllNames()
            )
        )
    )


def get_all_pd_elements_losses(distSys: SystemClass) -> pd.DataFrame:

    line_losses = get_all_line_losses(
        distSys
    )

    transformer_losses = get_all_transformers_losses(
        distSys
    )

    return pd.concat([transformer_losses, line_losses])


def get_total_pd_elements_losses(distSys: SystemClass) -> pd.DataFrame:
    data_loss = []
    data = {
        "name": "all_pd_elements",
        "kw_losses_total": sum(
            get_all_pd_elements_losses(distSys)['kw_losses']
        ),
        "kvar_losses_total": sum(
            get_all_pd_elements_losses(distSys)['kw_losses']
        ),
    }

    data_loss.append(data)
    return pd.DataFrame(data_loss)
