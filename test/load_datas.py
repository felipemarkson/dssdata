import pandas as pd


def load_data_static():
    with open("test/test_datas/bus_names.json") as json_file:
        bus_names = (
            pd.read_json(json_file, dtype="str")["bus_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/line_names.json") as json_file:
        line_names = (
            pd.read_json(json_file, dtype="str")["line_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/reg_names.json") as json_file:
        reg_names = (
            pd.read_json(json_file, dtype="str")["reg_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/all_v_pu_ang.json") as json_file:
        all_v_pu_ang = pd.read_json(
            json_file,
            dtype={
                "bus_name": str,
                "v_pu_a": float,
                "v_pu_b": float,
                "v_pu_c": float,
                "ang_a": float,
                "ang_b": float,
                "ang_c": float,
                "phase": str,
            },
        )

    with open("test/test_datas/all_line_infos.json") as json_file:
        all_line_infos = pd.read_json(
            json_file,
            dtype={
                "name": str,
                "bus1": str,
                "ph_bus1": str,
                "bus2": str,
                "ph_bus2": str,
                "I(A)_bus1_ph_a": float,
                "I(A)_bus1_ph_b": float,
                "I(A)_bus1_ph_c": float,
                "I(A)_bus2_ph_a": float,
                "I(A)_bus2_ph_b": float,
                "I(A)_bus2_ph_c": float,
                "ang_bus1_ph_a": float,
                "ang_bus1_ph_b": float,
                "ang_bus1_ph_c": float,
                "ang_bus2_ph_a": float,
                "ang_bus2_ph_b": float,
                "ang_bus2_ph_c": float,
                "kw_losses": float,
                "kvar_losses": float,
                "emergAmps": float,
                "normAmps": float,
                "perc_NormAmps": float,
                "perc_EmergAmps": float,
            },
        )

    with open("test/test_datas/taps_number.json") as json_file:
        taps_number = pd.read_json(
            json_file, dtype={"reg_name": str, "tap": int}
        )

    return (
        bus_names,
        line_names,
        reg_names,
        all_v_pu_ang,
        all_line_infos,
        taps_number,
    )


def load_data_TS():

    with open("test/test_datas/bus_names.json") as json_file:
        bus_names = (
            pd.read_json(json_file, dtype="str")["bus_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/line_names.json") as json_file:
        line_names = (
            pd.read_json(json_file, dtype="str")["line_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/reg_names.json") as json_file:
        reg_names = (
            pd.read_json(json_file, dtype="str")["reg_name"]
            .sort_index()
            .tolist()
        )

    with open("test/test_datas/v_pu_ang_all_13busTS.json") as json_file:
        all_v_pu_ang = pd.read_json(
            json_file,
            dtype={
                "bus_name": str,
                "v_pu_a": float,
                "v_pu_b": float,
                "v_pu_c": float,
                "ang_a": float,
                "ang_b": float,
                "ang_c": float,
                "phase": str,
                "step": int,
            },
        )

    with open("test/test_datas/line_infos_all_13busTS.json") as json_file:
        all_line_infos = pd.read_json(
            json_file,
            dtype={
                "name": str,
                "bus1": str,
                "ph_bus1": str,
                "bus2": str,
                "ph_bus2": str,
                "I(A)_bus1_ph_a": float,
                "I(A)_bus1_ph_b": float,
                "I(A)_bus1_ph_c": float,
                "I(A)_bus2_ph_a": float,
                "I(A)_bus2_ph_b": float,
                "I(A)_bus2_ph_c": float,
                "ang_bus1_ph_a": float,
                "ang_bus1_ph_b": float,
                "ang_bus1_ph_c": float,
                "ang_bus2_ph_a": float,
                "ang_bus2_ph_b": float,
                "ang_bus2_ph_c": float,
                "kw_losses": float,
                "kvar_losses": float,
                "emergAmps": float,
                "normAmps": float,
                "perc_NormAmps": float,
                "perc_EmergAmps": float,
                "step": int,
            },
        )

    with open("test/test_datas/taps_numberTS.json") as json_file:
        taps_number = pd.read_json(
            json_file, dtype={"reg_name": str, "tap": int, "step": int}
        )

    with open("test/test_datas/taps_changesTS.json") as json_file:
        taps_chgs = pd.read_json(
            json_file, dtype={"reg_name": str, "tap": int}
        )

    return (
        bus_names,
        line_names,
        reg_names,
        all_v_pu_ang,
        all_line_infos,
        taps_number,
        taps_chgs,
    )
