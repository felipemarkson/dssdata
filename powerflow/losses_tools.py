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
            distSys.dss.CktElement.Losses()[0] / 1000, 3
        )
        kVar_Losses_Total = kVar_Losses_Total + round(
            distSys.dss.CktElement.Losses()[1] / 1000, 3
        )
        distSys.dss.PDElements.Next()

    data = {
        "name": "all_pd_elements",
        "kw_losses_total": kW_Losses_Total,
        "kvar_losses_total": kVar_Losses_Total,
    }

    data_loss.append(data)
    return pd.DataFrame(data_loss)
