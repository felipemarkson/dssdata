import opendssdirect
import pandas as pd
from os import getcwd, chdir


class PowerFlow:
    def __init__(self, path: str, kV, loadmult: float = 1):
        try:
            open(path, 'r')
        except FileNotFoundError:
            raise Exception("O arquivo não existe")

        self.__path = path
        self.__kV = kV
        self.dss = opendssdirect
        self.__loadmult = loadmult

    def get_path(self):
        return self.__path

    def get_kV(self):
        return self.__kV

    def get_loadmult(self):
        return self.__loadmult

    def run_power_flow(self):
        directory = getcwd()
        self.dss.run_command(f"Compile {self.__path}")
        self.dss.run_command(f"Set voltagebases={self.__kV}")
        self.dss.run_command("calcv")
        self.dss.run_command(f"Set loadmult = {self.__loadmult}")
        self.dss.Solution.Solve()
        chdir(directory)

    def get_erros(self):
        return self.dss.Error.Description()

    def get_all_bus_names(self):
        return self.dss.Circuit.AllBusNames()

    def get_all_v_pu_angle_pandas(self):
        all_v_pu = self.__get_all_v_pu()
        all_ang = self.__get_all_ang()

        df_bus_names = pd.DataFrame(
            self.get_all_bus_names(), columns=['bus_names'])
        df_v_pu = pd.DataFrame(
            all_v_pu, columns=['v_pu_a', 'v_pu_b', 'v_pu_c'])
        df_ang = pd.DataFrame(all_ang, columns=['ang_a', 'ang_b', 'ang_c'])
        result = pd.concat([df_bus_names, df_v_pu, df_ang], axis=1, sort=False)

        result['phases'] = self.__get_all_num_ph()
        return result

    def get_bus_v_pu_ang_pandas(self,  buses: list):
        list_verify = self.__verify_bus_list(buses)
        if not all(list_verify):
            for (verify, bus) in zip(list_verify, buses):
                if not verify:
                    raise Exception(
                        f"A barra {bus} não está declarada no sistema")

        v_pu_list = []
        ang_list = []
        ph_list = []

        for bus in buses:
            ang_list.append(self.__get_bus_ang(bus))
            v_pu_list.append(self.__get_bus_v_pu(bus))
            ph = self.__get_bus_ph(bus)
            ph_config = self.__identify_ph_config(ph)
            ph_list.append(ph_config)

        df_bus_names = pd.DataFrame(buses, columns=['bus_names'])
        df_v_pu = pd.DataFrame(v_pu_list, columns=[
                               'v_pu_a', 'v_pu_b', 'v_pu_c'])
        df_ang = pd.DataFrame(ang_list, columns=['ang_a', 'ang_b', 'ang_c'])
        df_ph = pd.DataFrame(ph_list, columns=['phases'])

        result = pd.concat(
            [df_bus_names, df_v_pu, df_ang, df_ph], axis=1, sort=False)
        return result

    def get_all_lines_names(self):
        return self.dss.Lines.AllNames()

    def get_line_infos(self, lines_names: list):

        def vanish_line_infos(bus_raw: list, current_raw: list):
            bus_name = bus_raw[0]
            phs_raw = list(map(lambda bus: int(bus), bus_raw[1:]))
            if phs_raw == []:
                phs_raw = [1, 2, 3]
            phs = self.__identify_ph_config(phs_raw)
            currents_mag = self.__get_mag_vanish(
                phs_raw, bus_name, current_raw)
            currents_ang = self.__get_ang_vanish(
                phs_raw, bus_name, current_raw)

            return (bus_name, phs, currents_mag, currents_ang)

        data_list = []

        for line_name in lines_names:
            self.dss.Lines.Name(line_name)
            losses = self.dss.CktElement.Losses()
            normalAmps = self.dss.CktElement.NormalAmps()
            emergAmps = self.dss.CktElement.EmergAmps()
            currents_raw = self.dss.CktElement.CurrentsMagAng()
            currents_raw_bus1 = currents_raw[:int(len(currents_raw)/2)]
            currents_raw_bus2 = currents_raw[int(len(currents_raw)/2):]

            bus_raw = self.dss.Lines.Bus1().split('.')
            (bus_name1, phs1,
             currents_mag1, currents_ang1) = vanish_line_infos(
                bus_raw, currents_raw_bus1)
            bus_raw = self.dss.Lines.Bus2().split('.')
            (bus_name2, phs2,
             currents_mag2, currents_ang2) = vanish_line_infos(
                bus_raw, currents_raw_bus2)

            currents_mag1_calc = currents_mag1.copy()
            while None in currents_mag1_calc:
                currents_mag1_calc.remove(None)
            currents_mag2_calc = currents_mag2.copy()
            while None in currents_mag2_calc:
                currents_mag2_calc.remove(None)

            data = {
                'name': line_name,
                'bus1': bus_name1,
                'ph_bus1': phs1,
                'bus2': bus_name2,
                'ph_bus2': phs2,
                'I(A)_bus1_ph_a': round(currents_mag1[0], 3)
                if currents_mag1[0] is not None else None,
                'I(A)_bus1_ph_b': round(currents_mag1[1], 3)
                if currents_mag1[1] is not None else None,
                'I(A)_bus1_ph_c': round(currents_mag1[2], 3)
                if currents_mag1[2] is not None else None,
                'I(A)_bus2_ph_a': round(currents_mag2[0], 3)
                if currents_mag2[0] is not None else None,
                'I(A)_bus2_ph_b': round(currents_mag2[1], 3)
                if currents_mag2[1] is not None else None,
                'I(A)_bus2_ph_c': round(currents_mag2[2], 3)
                if currents_mag2[2] is not None else None,
                'ang_bus1_ph_a': round(currents_ang1[0], 2)
                if currents_ang1[0] is not None else None,
                'ang_bus1_ph_b': round(currents_ang1[1], 2)
                if currents_ang1[1] is not None else None,
                'ang_bus1_ph_c': round(currents_ang1[2], 2)
                if currents_ang1[2] is not None else None,
                'ang_bus2_ph_a': round(currents_ang2[0], 2)
                if currents_ang2[0] is not None else None,
                'ang_bus2_ph_b': round(currents_ang2[1], 2)
                if currents_ang2[1] is not None else None,
                'ang_bus2_ph_c': round(currents_ang2[2], 2)
                if currents_ang2[2] is not None else None,
                'kw_losses': round(losses[0]/1000, 3),
                'kvar_losses': round(losses[1]/1000, 3),
                'emergAmps': round(emergAmps, 3),
                'normAmps': round(normalAmps, 3),
                'perc_NormAmps': round(
                    max(
                        currents_mag1_calc + currents_mag2_calc)/normalAmps, 3
                    ),
                'perc_EmergAmps': round(
                    max(
                        currents_mag1_calc + currents_mag2_calc)/emergAmps, 3
                    ),
            }
            data_list.append(data)

        return pd.DataFrame(data_list)

    def get_all_line_infos(self):
        line_names = self.get_all_lines_names()
        return self.get_line_infos(line_names)

    def __verify_bus_list(self, buses: list):
        all_bus_names = self.get_all_bus_names()
        verify_per_bus = list(map(lambda bus: bus in all_bus_names, buses))
        return verify_per_bus

    def __get_bus_v_pu_ang(self, bus: str):
        self.dss.Circuit.SetActiveBus(bus)
        return self.dss.Bus.puVmagAngle()

    def __get_bus_ph(self, bus: str):
        self.dss.Circuit.SetActiveBus(bus)
        return self.dss.Bus.Nodes()

    def __get_mag_vanish(self, list_ph: list, bus: str, data: list):
        mag = [None, None, None]
        mag_dss = []
        for indx in range(0, len(data), 2):
            mag_dss.append(data[indx])

        indx = 0
        for ph in list_ph:
            mag[ph-1] = round(mag_dss[indx], 5)
            indx += 1

        return mag

    def __get_ang_vanish(self, list_ph: list, bus: str, data: list):
        ang = [None, None, None]
        ang_dss = []

        for indx in range(1, len(data)+1, 2):
            ang_dss.append(data[indx])

        indx = 0
        for ph in list_ph:
            ang[ph-1] = round(ang_dss[indx], 1)
            indx += 1

        return ang

    def __get_bus_v_pu(self, bus: str):
        v_pu_ang_dss = self.__get_bus_v_pu_ang(bus)
        list_ph = self.__get_bus_ph(bus)
        v_pu = self.__get_mag_vanish(list_ph, bus, v_pu_ang_dss)
        return v_pu

    def __get_bus_ang(self, bus: str):
        v_pu_ang_dss = self.__get_bus_v_pu_ang(bus)
        list_ph = self.__get_bus_ph(bus)
        ang = self.__get_ang_vanish(list_ph, bus, v_pu_ang_dss)
        return ang

    def __get_all_v_pu(self):
        all_bus_names = self.get_all_bus_names()
        all_v_pu = []
        for bus in all_bus_names:
            v_pu = self.__get_bus_v_pu(bus)
            all_v_pu.append(v_pu)

        return all_v_pu

    def __get_all_ang(self):
        all_bus_names = self.get_all_bus_names()
        all_ang = []
        for bus in all_bus_names:
            ang = self.__get_bus_ang(bus)
            all_ang.append(ang)

        return all_ang

    def __get_all_num_ph(self):
        all_bus_names = self.get_all_bus_names()
        all_num_ph = []
        for bus in all_bus_names:
            ph = self.__get_bus_ph(bus)
            ph_config = self.__identify_ph_config(ph)

            all_num_ph.append(ph_config)

        return all_num_ph

    def __identify_ph_config(self, ph: list):

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
