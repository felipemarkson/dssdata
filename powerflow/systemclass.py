import opendssdirect
from os import getcwd, chdir
from os import path as pathfunc
from .decorators import pf_tools


class SystemClass(object):
    """
    TODO:   Na ultima versão quando lançar o build, trocar o nome path
            para outro e alterar o import pathfunc
    """

    def __init__(self, *, path: str, kV, loadmult: float = 1):
        try:
            with open(path, "rt") as file:
                self._dsscontent = file.read().splitlines()
        except FileNotFoundError:
            raise Exception("O arquivo não existe")
        self.__path = path
        self.__folder = pathfunc.split(path)[0]
        self.__dss_file = pathfunc.split(path)[1]
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

    def run_command(self, cmd: str):
        self.dss.run_command(cmd)
        erro = self.dss.Error.Description()
        if erro != "":
            raise Exception(erro)

    def compile(self):
        directory = getcwd()
        self.dss.Basic.ClearAll()
        chdir(self.__folder)
        list(map(lambda cmd: self.run_command(cmd), self._dsscontent,))
        chdir(directory)
        self.run_command(f"Set voltagebases={self.__kV}")
        self.run_command("calcv")
        self.run_command(f"Set loadmult = {self.__loadmult}")

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
