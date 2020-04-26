import pandas as pd
from .systemclass import SystemClass


def get_total_pd_elements_losses(distSys: SystemClass):
    data_loss = []
    capacitors = distSys.dss.Capacitors.AllNames()
    distSys.dss.PDElements.First()
    kW_Losses_Total = 0
    kVar_Losses_Total = 0
    for pd_el in range(distSys.dss.PDElements.Count()):
        if (
            distSys.dss.PDElements.Name().replace("Capacitor.", "")
            in capacitors
        ):
            distSys.dss.PDElements.Next()
            continue
        kW_Losses_Total = kW_Losses_Total + round(
            distSys.dss.CktElement.Losses()[0] / 1000, 4
        )
        kVar_Losses_Total = kVar_Losses_Total + round(
            distSys.dss.CktElement.Losses()[1] / 1000, 4
        )
        distSys.dss.PDElements.Next()

    data = {
        "name": "all_pd_elements",
        "kw_losses_total": kW_Losses_Total,
        "kvar_losses_total": kVar_Losses_Total,
    }

    data_loss.append(data)
    return pd.DataFrame(data_loss)


def get_all_pd_elements_losses(distSys: SystemClass):
    capacitors = distSys.dss.Capacitors.AllNames()
    data_loss = []
    distSys.dss.PDElements.First()
    for pd_el in range(distSys.dss.PDElements.Count()):
        if (
            distSys.dss.PDElements.Name().replace("Capacitor.", "")
            in capacitors
        ):
            distSys.dss.PDElements.Next()
            continue
        data_aux = {
            'name': distSys.dss.PDElements.Name(),
            'kw_loss': round(distSys.dss.CktElement.Losses()[0] / 1000, 4),
            'kvar_loss': round(distSys.dss.CktElement.Losses()[1] / 1000, 4),
            }
        data_loss.append(data_aux.copy())
        distSys.dss.PDElements.Next()
    data_aux = {
        'name': 'total_pd_elements_losses',
        'kw_loss': (
            get_total_pd_elements_losses(distSys)['kw_losses_total'][0]
            ),
        'kvar_loss': (
            get_total_pd_elements_losses(distSys)['kvar_losses_total'][0]
            ),
        }
    data_loss.append(data_aux.copy())

    return pd.DataFrame(data_loss)


def get_transformer_losses(distSys: SystemClass):
    if distSys.dss.Transformers.Count() > 0:
        transformers_losses = []
        kW_transformers_total = 0
        kVar_transformers_total = 0
        distSys.dss.Transformers.First()
        for pd_trafos in range(distSys.dss.Transformers.Count()):
            kW_transformers_total = kW_transformers_total + round(
                distSys.dss.CktElement.Losses()[0] / 1000, 4
                )
            kVar_transformers_total = kVar_transformers_total + round(
                distSys.dss.CktElement.Losses()[1] / 1000, 4
                )
            data_trafo = {
                'name': distSys.dss.Transformers.Name(),
                'kw_loss': round(
                    distSys.dss.CktElement.Losses()[0]/1000, 4
                    ),
                'kvar_loss': round(
                    distSys.dss.CktElement.Losses()[1]/1000, 4
                    ),
            }

            transformers_losses.append(data_trafo.copy())
            distSys.dss.Transformers.Next()

        data_trafo = {
            'name': 'total_transformers_losses',
            'kw_loss': kW_transformers_total,
            'kvar_loss': kVar_transformers_total,
        }

        transformers_losses.append(data_trafo.copy())
    else:
        return print(
            "Não foram encontrados transformadores conectados à rede."
            )

    return pd.DataFrame(transformers_losses)
