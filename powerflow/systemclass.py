import opendssdirect
from os import getcwd, chdir
from os import path as pathfunc
from .decorators import pf_tools


class SystemClass(object):
    """
    TODO:   Na ultima versão quando lançar o build, trocar o nome path
            para outro e alterar o import pathfunc
    TODO:   Na ultima versão quando lançar o build.
            Utilizar o @propetry na classe.
    """

    def __init__(self, *, path: str, kV, loadmult: float = 1):
        try:
            with open(path, "rt") as file:
                self._dsscontent = file.read().splitlines()
        except FileNotFoundError as err:
            raise err
        self.__path = path
        self.__folder = pathfunc.split(path)[0]
        self.__dss_file = pathfunc.split(path)[1]
        self.__kV = kV
        self.__dss = opendssdirect
        self.__loadmult = loadmult
        self.init_sys()
        self.__name = self.dss.Circuit.Name()

    @property
    def dss(self):
        return self.__dss

    @property
    def dsscontent(self):
        return self._dsscontent

    @dsscontent.setter
    def dsscontent(self, content):
        self._dsscontent = content

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
        erro = self.get_erros()
        if erro != "":
            raise Exception(erro)

    def cfg_system(self):
        self.run_command(f"Set voltagebases={self.__kV}")
        self.run_command("calcv")
        self.run_command(f"Set loadmult = {self.__loadmult}")

    def init_sys(self):
        directory = getcwd()
        self.dss.Basic.ClearAll()
        if self.__folder != "":
            chdir(self.__folder)
            list(map(self.run_command, self.dsscontent,))
            chdir(directory)
        else:
            list(map(self.run_command, self.dsscontent,))
        self.cfg_system()

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
