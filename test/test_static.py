import unittest
from powerflow.systemclass import SystemClass
from powerflow.pf_modes import run_power_flow
from powerflow.line_tools import get_all_line_infos, get_line_infos
from powerflow.voltage_tools import get_all_v_pu_ang, get_bus_v_pu_ang
from pandas._testing import assert_frame_equal
from .load_datas import load_data_static


class Verifica_Voltage_tools(unittest.TestCase):
    def setUp(self):

        path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        run_power_flow(self.distSys)

        (
            self.bus_names,
            self.line_names,
            self.all_v_pu_ang,
            self.all_line_infos,
        ) = load_data_static()

    def test_get_all_v_pu_ang(self):
        df_all_bus = get_all_v_pu_ang(self.distSys)
        try:
            assert_frame_equal(
                self.all_v_pu_ang, df_all_bus, check_dtype=False
            )
        except AssertionError:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_get_bus_v_pu_ang(self):
        for bus_name in self.bus_names:
            df_bus = get_bus_v_pu_ang(self.distSys, [bus_name])
            v_pu_ang = self.all_v_pu_ang.loc[
                self.all_v_pu_ang["bus_name"] == bus_name
            ]
            try:
                assert_frame_equal(
                    v_pu_ang.reset_index(drop=True),
                    df_bus.reset_index(drop=True),
                    check_dtype=False,
                )
            except AssertionError:
                self.assertTrue(False)
        self.assertTrue(True)


class Verifica_line_tools(unittest.TestCase):
    def setUp(self):

        path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        run_power_flow(self.distSys)

        (
            self.bus_names,
            self.line_names,
            self.all_v_pu_ang,
            self.all_line_infos,
        ) = load_data_static()

    def test_get_all_lines_infos(self):
        df_all_lines = get_all_line_infos(self.distSys)
        try:
            assert_frame_equal(
                self.all_line_infos, df_all_lines, check_dtype=False,
            )
        except AssertionError:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_get_line_infos(self):
        for line_name in self.line_names:
            df_lines = get_line_infos(self.distSys, [line_name])
            line_infos = self.all_line_infos.loc[
                self.all_line_infos["name"] == line_name
            ]
            try:
                assert_frame_equal(
                    line_infos.reset_index(drop=True),
                    df_lines.reset_index(drop=True),
                    check_dtype=False,
                )
            except AssertionError as err:
                raise err
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
