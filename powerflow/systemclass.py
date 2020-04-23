import opendssdirect
from os import getcwd, chdir
from .decorators import pf_tools


class SystemClass:
    def __init__(self, path: str, kV, loadmult: float = 1):
        try:
            with open(path, "rt") as file:
                self._dsscontent = file.read().splitlines()
        except FileNotFoundError:
            raise Exception("O arquivo não existe")

        self.__path = path
        self.__kV = kV
        self.dss = opendssdirect
        self.__loadmult = loadmult
        self.compile()
        self.__name = self.dss.Circuit.Name()

    def get_name(self):
        return self.__name

    def get_path(self):
        return self.__path

    def get_kV(self):
        return self.__kV

    def get_loadmult(self):
        return self.__loadmult

    def compile(self):
        directory = getcwd()
        self.dss.Basic.ClearAll()
        newdir = self.__path[: self.__path.rfind(directory[0])]
        chdir(newdir)
        list(
            map(
                lambda command: self.dss.run_command(command), self._dsscontent
            )
        )
        erro = self.dss.Error.Description()
        if erro != "":
            raise Exception(erro)
        chdir(directory)
        self.dss.run_command(f"Set voltagebases={self.__kV}")
        self.dss.run_command("calcv")
        self.dss.run_command(f"Set loadmult = {self.__loadmult}")

    @pf_tools
    def get_erros(self):
        return self.dss.Error.Description()

    @pf_tools
    def get_all_bus_names(self):
        return self.dss.Circuit.AllBusNames()

    @pf_tools
    def get_all_lines_names(self):
        return self.dss.Lines.AllNames()

    @pf_tools
    def get_all_regs_names(self):
        return self.dss.RegControls.AllNames()
