from functools import partial


def __isodd(value):
    return value % 2 != 0


def __iseven(value):
    return value % 2 == 0


def __aux_vanish(list_ph: list, mag_or_ang: list, indx: int):
    try:
        return mag_or_ang[list_ph.index(indx + 1)]
    except ValueError:
        return None


def __get_mag_vanish(list_ph: list, data: list) -> tuple:
    # The mags is in even indexes
    mag_indexes = filter(__iseven, range(0, len(data)))

    mag_formatted = tuple(
        map(lambda indx: __format_mag(data[indx]), mag_indexes)
    )

    func_aux = partial(__aux_vanish, list_ph, mag_formatted)

    return tuple(map(func_aux, range(0, 3)))


def __get_ang_vanish(list_ph: list, data: list) -> tuple:
    # The angs is in isodd indexes
    ang_indexes = filter(__isodd, range(0, len(data)))

    ang_formatted = tuple(
        map(lambda indx: __format_ang(data[indx]), ang_indexes)
    )

    func_aux = partial(__aux_vanish, list_ph, ang_formatted)

    return tuple(map(func_aux, range(0, 3)))


def __identify_ph_config(phs: list) -> str:
    def aux_ph(ph: int):
        if ph == 1:
            return "a"
        elif ph == 2:
            return "b"
        elif ph == 3:
            return "c"
        else:
            raise Exception(
                f"The phase {ph} is not a valid number. "
                + "Only 1, 2 or 3 is aceppted."
            )

    return "".join(map(aux_ph, phs))


def __format_mag(value: float) -> float:
    return round(value, 4)  # Valor padrão do  OpenDSS


def __format_ang(value: float) -> float:
    return round(value, 2)  # Valor padrão do  OpenDSS


def __remove_nones_from_lists(data: list) -> tuple:
    return tuple(filter(lambda value: value is not None, data))


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
    for element_name in element_names:
        if element_name not in all_elements_names:
            raise ValueError(
                f"The element {element_name} is not declared"
                + "on distribution system"
            )
