import opendssdirect
import numpy as np
import pandas as pd

class OpenDSS:
    def __init__(self, path:str , kV:float, loadmult:float):
        try:
            open(path,'r')
        except:
            raise Exception("O arquivo não existe")
        
        try:
            float(kV)
        except:
            raise Exception("O valor de kV não é um número ou não pode ser convertido em um número")
        self.__path = path
        self.__kV = kV
        self.__dss = opendssdirect
        self.__loadmult = loadmult


    def get_path(self):
        return self.__path

    def run_openDSS(self):
        
        self.__dss.run_command(f"Compile {self.__path}")
        self.__dss.run_command(f"Set voltagebases=[{self.__kV}]")
        self.__dss.run_command("calcv")
        self.__dss.run_command("Set loadmult = 100000")
        self.__dss.Solution.Solve()

    def get_erros(self):
        self.__dss.Error.Description()

    def get_all_bus_names(self):
        return self.__dss.Circuit.AllBusNames()

    def get_bus_v_pu_ang(self, bus: str):
        self.__dss.Circuit.SetActiveBus(bus)
        return self.__dss.Bus.puVmagAngle()

    def get_bus_ph(self, bus: str):
        return self.__dss.Bus.Nodes()

    def get_bus_v_pu(self, bus: str):
        v_pu_ang_dss = self.get_bus_v_pu_ang(bus)
        list_ph = self.get_bus_ph(bus)
        v_pu = [np.NaN , np.NaN , np.NaN]
        v_pu_dss = []
        for indx in range(0, len(v_pu_ang_dss), 2):
            v_pu_dss.append(v_pu_ang_dss[indx])
        
        indx = 0
        for ph in list_ph:
            v_pu[ph-1] = v_pu_dss[indx]
            indx += 1

        return v_pu

    def get_bus_ang(self, bus: str):
        v_pu_ang_dss = self.get_bus_v_pu_ang(bus)
        list_ph = self.get_bus_ph(bus)
        ang = [np.NaN  , np.NaN , np.NaN ]    
        ang_dss = []

        for indx in range(1, len(v_pu_ang_dss)+1, 2):
            ang_dss.append(v_pu_ang_dss[indx])
        
        indx = 0
        for ph in list_ph:
            ang[ph-1] = ang_dss[indx]
            indx += 1

        return ang


    def get_all_v_pu(self):
        all_bus_names = self.get_all_bus_names()
        all_v_pu = []
        for bus in all_bus_names:
            v_pu = self.get_bus_v_pu(bus)
            all_v_pu.append(v_pu)

        return all_v_pu

    def get_all_v_pu_pandas(self):    
        all_v_pu = self.get_all_v_pu()
        all_bus_names = self.get_all_bus_names()
        df = pd.DataFrame(all_v_pu, columns =['ph_a','ph_b', 'ph_c'])
        df['bus_names'] = all_bus_names        
        return df