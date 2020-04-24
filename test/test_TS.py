import unittest
from powerflow.systemclass import SystemClass
from powerflow.pf_modes import cfg_tspf, buil_dataset_tspf

from powerflow.line_tools import get_all_line_infos, get_line_infos
from powerflow.voltage_tools import get_all_v_pu_ang, get_bus_v_pu_ang
from powerflow.reg_tools import (
    get_all_taps_number,
    get_tap_number,
    get_taps_changes,
)
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

    def test_buil_dataset_tspf_v_pu(self):

        [df_all_v_pu_ang] = buil_dataset_tspf(
            self.distSys, funcs_list=[get_all_v_pu_ang], num_steps=288
        )

        try:
            assert_frame_equal(
                self.all_v_pu_ang, df_all_v_pu_ang, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_get_bus_v_pu_ang(self):
        def get_one(distSys):
            return get_bus_v_pu_ang(distSys, self.bus_names)

        [df_v_pu_ang] = buil_dataset_tspf(
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

    def test_build_dataset_tspf_line_infos(self):

        [df_all_line_infos] = buil_dataset_tspf(
            self.distSys, funcs_list=[get_all_line_infos], num_steps=288
        )

        try:
            assert_frame_equal(
                self.all_line_infos, df_all_line_infos, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_get_bus_v_pu_ang(self):
        def get_one(distSys):
            return get_line_infos(distSys, self.line_names)

        [df_all_line_infos] = buil_dataset_tspf(
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

        [df_all_taps_number] = buil_dataset_tspf(
            self.distSys, funcs_list=[get_all_taps_number], num_steps=288
        )

        try:
            assert_frame_equal(
                self.reg_number, df_all_taps_number, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_build_dataset_tspf_taps_number(self):
        def get_one(distSys):
            return get_tap_number(distSys, self.reg_names)

        [df_all_taps_number] = buil_dataset_tspf(
            self.distSys, funcs_list=[get_one], num_steps=288
        )

        try:
            assert_frame_equal(
                self.reg_number, df_all_taps_number, check_dtype=False
            )
        except AssertionError as err:
            raise err

    def test_buil_dataset_tspf_taps_chngs(self):
        df_taps_chngs = get_taps_changes(self.reg_number)
        try:
            assert_frame_equal(
                self.reg_chngs, df_taps_chngs, check_dtype=False
            )
        except AssertionError as err:
            raise err


if __name__ == "__main__":
    unittest.main()
