def __get_mag_vanish(list_ph: list, data: list):
    mag = [None, None, None]
    mag_dss = []
    for indx in range(0, len(data), 2):
        mag_dss.append(data[indx])

    indx = 0
    for ph in list_ph:
        mag[ph - 1] = __format_mag(mag_dss[indx])
        indx += 1

    return mag


def __get_ang_vanish(list_ph: list, data: list):
    ang = [None, None, None]
    ang_dss = []

    for indx in range(1, len(data) + 1, 2):
        ang_dss.append(data[indx])

    indx = 0
    for ph in list_ph:
        ang[ph - 1] = __format_ang(ang_dss[indx])
        indx += 1

    return ang


def __identify_ph_config(ph: list):

    if ph == [1, 2, 3]:
        ph_config = "abc"
    elif ph == [1, 2]:
        ph_config = "ab"
    elif ph == [1, 3]:
        ph_config = "ac"
    elif ph == [2, 3]:
        ph_config = "bc"
    elif ph == [1]:
        ph_config = "a"
    elif ph == [2]:
        ph_config = "b"
    elif ph == [3]:
        ph_config = "c"
    elif ph == []:
        ph_config = "abc"
    else:
        raise Exception(f"Configuração de fases {ph} não identificada")
    return ph_config


def __format_mag(value: float) -> float:
    return round(value, 4)  # Valor padrão do  OpenDSS


def __format_ang(value: float) -> float:
    return round(value, 2)  # Valor padrão do  OpenDSS


def __remove_nones_from_lists(data: list) -> list:
    data_new = data.copy()
    while None in data_new:
        data_new.remove(None)
    return data_new


def __check_elements(element_names: list, all_elements_names: list) -> None:
    """
    Verifica se todos os elementos da lista estão em um outra lista.
    Args:
        element_names: lista menor a ser verificada.
        all_elements_names:lista maior contendo todo o conteúdo
    Returns:
        None
    Raises:
        Exception:  Se algum item de element_names não estiver em
                    all_elements_names
    """

    def check_one(element_name):
        if element_name not in all_elements_names:
            raise Exception(
                f"O Elemento {element_name} não está declarado no sistema"
            )

    list(map(check_one, element_names))
