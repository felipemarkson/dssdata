import pandas as pd


def load_loss_data():
    with open('test/test_datas/losses_data.json') as j_file:
        pd_losses = pd.read_json(
            j_file,
            dtype={
                "type": str,
                "name": str,
                "kw_losses": float,
                "kvar_losses": float,
            },
        )

    with open('test/test_datas/element_loss_data.json') as j_file:
        pd_element_loss = pd.read_json(
            j_file,
            dtype={
                "type": str,
                "name": str,
                "kw_losses": float,
                "kvar_losses": float,
            },
        )

    with open('test/test_datas/lines_loss_data.json') as j_file:
        pd_line_losses = pd.read_json(
            j_file,
            dtype={
                "type": str,
                "name": str,
                "kw_losses": float,
                "kvar_losses": float,
            },
        )

    with open('test/test_datas/trafo_loss_data.json') as j_file:
        pd_trafos_losses = pd.read_json(
            j_file,
            dtype={
                "type": str,
                "name": str,
                "kw_losses": float,
                "kvar_losses": float,
            },
        )

    with open('test/test_datas/total_loss_data.json') as j_file:
        pd_total_losses = pd.read_json(
            j_file,
            dtype={
                "name": str,
                "kw_losses_total": float,
                "kvar_losses_total": float,
            },
        )

    return (
        pd_losses,
        pd_element_loss,
        pd_line_losses,
        pd_trafos_losses,
        pd_total_losses,
    )
