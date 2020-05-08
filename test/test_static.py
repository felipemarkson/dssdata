import unittest
from dssdata import SystemClass
from dssdata.pfmodes import run_static_pf
from dssdata.tools import lines, voltages, regs
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

        (
            self.bus_names,
            self.line_names,
            _,
            self.all_v_pu_ang,
            _,
            _,
        ) = load_data_static()

    def test_get_all_v_pu_ang(self):
        [df_all_bus] = run_static_pf(self.distSys, tools=[voltages.get_all])
        try:
            assert_frame_equal(
                self.all_v_pu_ang, df_all_bus, check_dtype=False
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_get_bus_v_pu_ang(self):
        for bus_name in self.bus_names:
            [df_bus] = run_static_pf(
                self.distSys,
                tools=[
                    lambda distSys: voltages.get_from_buses(
                        distSys, [bus_name]
                    )
                ],
            )
            # df_bus = voltages.get_from_buses(self.distSys, [bus_name])
            v_pu_ang = self.all_v_pu_ang.loc[
                self.all_v_pu_ang["bus_name"] == bus_name
            ]
            try:
                assert_frame_equal(
                    v_pu_ang.reset_index(drop=True),
                    df_bus.reset_index(drop=True),
                    check_dtype=False,
                )
            except AssertionError as err:
                raise err
        self.assertTrue(True)


class Verifica_line_tools(unittest.TestCase):
    def setUp(self):

        path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        (
            self.bus_names,
            self.line_names,
            _,
            _,
            self.all_line_infos,
            _,
        ) = load_data_static()

    def test_get_all_lines_infos(self):
        [df_all_lines] = run_static_pf(
            self.distSys, tools=[lines.get_all_infos]
        )
        try:
            assert_frame_equal(
                self.all_line_infos, df_all_lines, check_dtype=False,
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_get_line_infos(self):
        for line_name in self.line_names:
            [df_lines] = run_static_pf(
                self.distSys,
                tools=[lambda distSys: lines.get_infos(distSys, [line_name])],
            )
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


class Verifica_reg_tools(unittest.TestCase):
    def setUp(self):

        path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        (
            self.bus_names,
            self.line_names,
            self.reg_names,
            _,
            _,
            self.all_taps_number,
        ) = load_data_static()

    def test_get_all_taps_number(self):
        [df_all_taps_number] = run_static_pf(
            self.distSys, tools=[regs.get_all_taps_number]
        )
        try:
            assert_frame_equal(
                self.all_taps_number, df_all_taps_number, check_dtype=False,
            )
        except AssertionError as err:
            raise err
        self.assertTrue(True)

    def test_get_tap_number(self):
        for reg_name in self.reg_names:
            [df_tap_number] = run_static_pf(
                self.distSys,
                tools=[lambda distSys: regs.get_tap_number(distSys, [reg_name])],
            )
            tap_number = self.all_taps_number.loc[
                self.all_taps_number["reg_name"] == reg_name
            ]
            try:
                assert_frame_equal(
                    tap_number.reset_index(drop=True),
                    df_tap_number.reset_index(drop=True),
                    check_dtype=False,
                )
            except AssertionError as err:
                raise err
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
