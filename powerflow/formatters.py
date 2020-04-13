def __get_mag_vanish(list_ph: list, data: list):
    mag = [None, None, None]
    mag_dss = []
    for indx in range(0, len(data), 2):
        mag_dss.append(data[indx])

    indx = 0
    for ph in list_ph:
        mag[ph-1] = round(mag_dss[indx], 5)
        indx += 1

    return mag


def __get_ang_vanish(list_ph: list, data: list):
    ang = [None, None, None]
    ang_dss = []

    for indx in range(1, len(data)+1, 2):
        ang_dss.append(data[indx])

    indx = 0
    for ph in list_ph:
        ang[ph-1] = round(ang_dss[indx], 1)
        indx += 1

    return ang


def __identify_ph_config(ph: list):

    if ph == [1, 2, 3]:
        ph_config = 'abc'
    elif ph == [1, 2]:
        ph_config = 'ab'
    elif ph == [1, 3]:
        ph_config = 'ac'
    elif ph == [2, 3]:
        ph_config = 'bc'
    elif ph == [1]:
        ph_config = 'a'
    elif ph == [2]:
        ph_config = 'b'
    elif ph == [3]:
        ph_config = 'c'
    else:

        raise Exception(f'Configuração de fases {ph} não identificada')
    return ph_config
