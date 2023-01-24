import unittest
from dssdata import SystemClass
from dssdata.pfmodes import run_static_pf
from dssdata.tools import losses
from .utils import assert_df_no_ang
from .load_loss_data import load_loss_data


class Verifica_Losses_Tools(unittest.TestCase):
    def setUp(self):

        path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        (
            self.pd_losses,
            self.pd_element_loss,
            self.pd_line_losses,
            self.pd_trafos_losses,
            self.pd_total_losses,
        ) = load_loss_data()

    def test_pd_element_loss(self):
        [element_loss] = run_static_pf(
            self.distSys,
            tools=[
                lambda distSys: losses.pd_element_loss(
                    self.distSys,
                    element_name="xfm1",
                    element_type="Transformer",
                )
            ],
        )
        try:
            assert_df_no_ang(
                self.pd_element_loss, element_loss
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_pd_list_loss(self):
        [element_list_loss] = run_static_pf(
            self.distSys,
            tools=[
                lambda distSys: losses.pd_element_loss_list(
                    self.distSys,
                    distSys.dss.Transformers.AllNames(),
                    element_type="Transformer",
                )
            ],
        )
        try:
            assert_df_no_ang(
                self.pd_trafos_losses.reset_index(drop=True),
                element_list_loss.reset_index(drop=True),
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_pd_loss(self):
        [LossDataFrame] = run_static_pf(
            self.distSys, tools=[losses.get_all_pd_elements_losses]
        )
        try:
            assert_df_no_ang(
                self.pd_losses.reset_index(drop=True),
                LossDataFrame.reset_index(drop=True),
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_line_loss(self):
        [LinesDataFrame] = run_static_pf(
            self.distSys, tools=[losses.get_all_line_losses]
        )
        try:
            assert_df_no_ang(
                self.pd_line_losses.reset_index(drop=True),
                LinesDataFrame.reset_index(drop=True),
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_trafo_loss(self):
        [TrafoDataFrame] = run_static_pf(
            self.distSys, tools=[losses.get_all_transformers_losses]
        )
        try:
            assert_df_no_ang(
                self.pd_trafos_losses.reset_index(drop=True),
                TrafoDataFrame.reset_index(drop=True),
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_total_loss(self):
        [TotalDataFrame] = run_static_pf(
            self.distSys, tools=[losses.get_total_pd_elements_losses]
        )
        try:
            assert_df_no_ang(
                self.pd_total_losses.reset_index(drop=True),
                TotalDataFrame,
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
