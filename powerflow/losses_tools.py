import pandas as pd
from .systemclass import SystemClass


def build_pd_dicts(
    distSys: SystemClass, element_name: str, element_type: str
) -> dict:

    if element_type == 'transformer':
        distSys.dss.Transformers.Name(element_name)
        typ = distSys.dss.CktElement.Name().replace("."+str(element_name), "")
    elif element_type == 'line':
        distSys.dss.Lines.Name(element_name)
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

    pd_loss = []
    pd_loss.append(
        build_pd_dicts(
            distSys, element_name, element_type
            )
    )
    return pd.DataFrame(pd_loss)


def get_all_line_losses(
    distSys: SystemClass, lines_names: list
) -> pd.DataFrame:
    element_type = 'line'

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: build_pd_dicts(
                    distSys, element_name, element_type
                ), lines_names
            )
        )
    )


def get_all_transformers_losses(
    distSys: SystemClass, transformes_names: list
) -> pd.DataFrame:
    element_type = 'transformer'

    return pd.DataFrame(
        tuple(
            map(
                lambda element_name: build_pd_dicts(
                    distSys, element_name, element_type
                ), transformes_names
            )
        )
    )


def get_all_pd_elements_losses(distSys: SystemClass) -> pd.DataFrame:

    line_losses = get_all_line_losses(
        distSys, distSys.dss.Lines.AllNames()
    )

    transformer_losses = get_all_transformers_losses(
        distSys, distSys.dss.Transformers.AllNames()
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
