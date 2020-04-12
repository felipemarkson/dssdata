import unittest
from powerflow import PowerFlow
import pandas as pd

path_of_system = 'test/syste_test_IEEE13bus/IEEE13Nodeckt.dss'
value_of_kV = [115, 4.16, .48]
value_of_load_mult = 1

bus_names = ['sourcebus', '650', 'rg60', '633', '634', '671', '645',
             '646', '692', '675', '611', '652', '670', '632', '680', '684']

line_names = ['650632', '632670', '670671', '671680', '632633',
              '632645', '645646', '692675', '671684', '684611', '684652',
              '671692']


distSys = PowerFlow(path=path_of_system, kV=value_of_kV,
                    loadmult=value_of_load_mult)
distSys.run_power_flow()


class Verifica_meth_gets(unittest.TestCase):

    def test_get_path(self):
        self.assertTrue(distSys.get_path() == path_of_system)

    def test_get_kV(self):
        self.assertTrue(distSys.get_kV() == value_of_kV)

    def test_get_loadmult(self):
        self.assertTrue(distSys.get_loadmult() == value_of_load_mult)

    def test_get_all_bus_names(self):
        self.assertTrue(bus_names == distSys.get_all_bus_names())

    def test_get_erros(self):
        self.assertTrue('' == distSys.get_erros())

    def test_get_bus_v_pu_ang_pandas(self):
        data = {
            'bus_names': ['684', '692'],
            'v_pu_a': [0.98087, 0.98279],
            'v_pu_b': [None, 1.04028],
            'v_pu_c': [0.96284, 0.96487],
            'ang_a': [-5.4, -5.4],
            'ang_b': [None, -122.4],
            'ang_c': [115.9, 116.0],
            'phases': ['ac', 'abc']
        }

        esperado = pd.DataFrame.from_dict(data)
        resultado = distSys.get_bus_v_pu_ang_pandas(['684', '692'])

        self.assertTrue(esperado.equals(resultado))

    def test_get_all_v_pu_ang_pandas(self):
        df_all_bus = distSys.get_all_v_pu_angle_pandas()
        df_buses_all = distSys.get_bus_v_pu_ang_pandas(bus_names)
        self.assertTrue(df_all_bus.equals(df_buses_all))

    def test_get_all_lines_names(self):
        self.assertEqual(line_names, distSys.get_all_lines_names())

    def test_get_line_infos(self):
        data = {
            'name': ['670671'],
            'bus1': ['670'],
            'ph_bus1': ['abc'],
            'bus2': ['671'],
            'ph_bus2': ['abc'],
            'I(A)_bus1_ph_a': [473.795],
            'I(A)_bus1_ph_b': [188.824],
            'I(A)_bus1_ph_c': [424.942],
            'I(A)_bus2_ph_a': [473.795],
            'I(A)_bus2_ph_b': [188.824],
            'I(A)_bus2_ph_c': [424.942],
            'ang_bus1_ph_a': [-27.0],
            'ang_bus1_ph_b': [-132.6],
            'ang_bus1_ph_c': [101.3],
            'ang_bus2_ph_a': [153.0],
            'ang_bus2_ph_b': [47.4],
            'ang_bus2_ph_c': [-78.7],
            'kw_losses': [22.729],
            'kvar_losses': [72.334],
            'emergAmps': [600.],
            'normAmps': [400.],
            'perc_NormAmps': [1.184],
            'perc_EmergAmps': [0.79]
        }
        esperado = pd.DataFrame(data)
        retorno = distSys.get_line_infos(['670671'])
        self.assertTrue(esperado.equals(retorno))

    def test_get_all_lines_infos(self):
        esperado = distSys.get_line_infos(line_names)
        retorno = distSys.get_all_line_infos()
        self.assertTrue(esperado.equals(retorno))