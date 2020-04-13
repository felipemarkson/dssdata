import opendssdirect
from os import getcwd, chdir


class SystemClass:
    def __init__(self, path: str, kV, loadmult: float = 1):
        try:
            open(path, 'r')
        except FileNotFoundError:
            raise Exception("O arquivo não existe")

        self.__path = path
        self.__kV = kV
        self.dss = opendssdirect
        self.__loadmult = loadmult
        self.__compile()
        if self.get_erros() != '':
            raise Exception(self.get_erros())

    def get_path(self):
        return self.__path

    def get_kV(self):
        return self.__kV

    def get_loadmult(self):
        return self.__loadmult

    def __compile(self):
        directory = getcwd()
        self.dss.run_command(f"Compile {self.__path}")
        self.dss.run_command(f"Set voltagebases={self.__kV}")
        self.dss.run_command("calcv")
        self.dss.run_command(f"Set loadmult = {self.__loadmult}")
        chdir(directory)

    def get_erros(self):
        return self.dss.Error.Description()

    def get_all_bus_names(self):
        return self.dss.Circuit.AllBusNames()

    def get_all_lines_names(self):
        return self.dss.Lines.AllNames()
