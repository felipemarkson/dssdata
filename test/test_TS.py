import unittest
from dssdata import SystemClass
from dssdata.pfmodes import cfg_tspf, build_dataset_tspf
from dssdata.tools import lines, voltages, regs
from dssdata._reduces import regs as reg_redc
from pandas._testing import assert_frame_equal
from .load_datas import load_data_TS


class Verifica_Voltage_toolsTS(unittest.TestCase):
    def setUp(self):

        path_of_system = (
            "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"
        )
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
            _,
        ) = load_data_TS()
        cfg_tspf(self.distSys, step_size="5m")

    def test_build_dataset_tspf_v_pu(self):

        [df_all_v_pu_ang] = build_dataset_tspf(
            self.distSys, funcs_list=[voltages.get_all], num_steps=288
        )

        try:
            assert_frame_equal(
                self.all_v_pu_ang, df_all_v_pu_ang, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_get_bus_v_pu_ang(self):
        def get_one(distSys):
            return voltages.get_from_buses(distSys, self.bus_names)

        [df_v_pu_ang] = build_dataset_tspf(
            self.distSys, funcs_list=[get_one], num_steps=288,
        )

        try:
            assert_frame_equal(
                self.all_v_pu_ang.reset_index(drop=True),
                df_v_pu_ang.reset_index(drop=True),
                check_dtype=False,
            )

        except AssertionError as err:
            raise err


class Verifica_Line_toolsTS(unittest.TestCase):
    def setUp(self):

        path_of_system = (
            "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"
        )
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
            _,
        ) = load_data_TS()
        cfg_tspf(self.distSys, step_size="5m")

    def test_build_dataset_tspf_line_all_infos(self):

        [df_all_line_infos] = build_dataset_tspf(
            self.distSys, funcs_list=[lines.get_all_infos], num_steps=288
        )

        try:
            assert_frame_equal(
                self.all_line_infos, df_all_line_infos, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_build_dataset_tspf_line_infos(self):
        def get_one(distSys):
            return lines.get_infos(distSys, self.line_names)

        [df_all_line_infos] = build_dataset_tspf(
            self.distSys, funcs_list=[get_one], num_steps=288,
        )

        try:
            assert_frame_equal(
                self.all_line_infos.reset_index(drop=True),
                df_all_line_infos.reset_index(drop=True),
                check_dtype=False,
            )

        except AssertionError as err:
            raise err


class Verifica_reg_toolsTS(unittest.TestCase):
    def setUp(self):
        path_of_system = (
            "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"
        )
        value_of_kV = [115, 4.16, 0.48]
        value_of_load_mult = 1

        self.distSys = SystemClass(
            path=path_of_system, kV=value_of_kV, loadmult=value_of_load_mult
        )

        (
            _,
            _,
            self.reg_names,
            _,
            _,
            self.reg_number,
            self.reg_chngs,
        ) = load_data_TS()
        cfg_tspf(self.distSys, step_size="5m")

    def test_buil_dataset_tspf_all_taps_number(self):

        [df_all_taps_number] = build_dataset_tspf(
            self.distSys, funcs_list=[regs.get_all_taps_number], num_steps=288
        )

        try:
            assert_frame_equal(
                self.reg_number, df_all_taps_number, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_build_dataset_tspf_taps_number(self):
        def get_one(distSys):
            return regs.get_tap_number(distSys, self.reg_names)

        [df_all_taps_number] = build_dataset_tspf(
            self.distSys, funcs_list=[get_one], num_steps=288
        )

        try:
            assert_frame_equal(
                self.reg_number, df_all_taps_number, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_buil_dataset_tspf_taps_chngs(self):
        df_taps_chngs = reg_redc.get_taps_changes(self.reg_number)
        try:
            assert_frame_equal(
                self.reg_chngs, df_taps_chngs, check_dtype=False
            )
        except AssertionError as err:
            raise err


if __name__ == "__main__":
    unittest.main()
