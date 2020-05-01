import unittest
from powerflow import SystemClass
from .load_datas import load_data_static


class Verifica_Class(unittest.TestCase):
    def setUp(self):

        self.path_of_system = "test/syste_test_IEEE13bus/IEEE13Nodeckt.dss"
        self.value_of_kV = [115, 4.16, 0.48]
        self.value_of_load_mult = 1

        self.distSys = SystemClass(
            path=self.path_of_system,
            kV=self.value_of_kV,
            loadmult=self.value_of_load_mult,
        )

        (
            self.bus_names,
            self.line_names,
            self.reg_names,
            _,
            _,
            _,
        ) = load_data_static()

    def test_get_path(self):
        self.assertTrue(self.distSys.get_path() == self.path_of_system)

    def test_get_kV(self):
        self.assertTrue(self.distSys.get_kV() == self.value_of_kV)

    def test_get_loadmult(self):
        self.assertTrue(self.distSys.get_loadmult() == self.value_of_load_mult)

    def test_get_all_bus_names(self):
        self.assertEqual(self.bus_names, self.distSys.get_all_bus_names())

    def test_get_all_lines_names(self):
        self.assertEqual(self.line_names, self.distSys.get_all_lines_names())

    def test_get_all_reg_names(self):
        self.assertEqual(self.reg_names, self.distSys.get_all_regs_names())


if __name__ == "__main__":
    unittest.main()
