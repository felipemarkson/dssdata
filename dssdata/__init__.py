from os import getcwd, chdir
from os import path as pathfunc
from .decorators import pf_tools as _pf
from typing import Iterable, List


class SystemClass(object):
    """
    The distribution system abstraction class.
    """  # noqa: E501

    """
    TODO:   Na ultima versão quando lançar o build, trocar o nome path
            para outro e alterar o import pathfunc
    TODO:   Na ultima versão quando lançar o build.
            Utilizar o @propetry na classe.
    """

    import opendssdirect

    def __init__(self, *, path: str, kV: Iterable[float], loadmult: float = 1):
        """
        Args:
            path (str): The path to the file that describes the distribution system.
            kV (Iterable[float]): The base voltages. See ```voltagebases``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf).
            loadmult (float, optional): The load multiplier.  See ```loadmult``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/> OpenDSSManual.pdf).
        """  # noqa: E501

        with open(path, "rt") as file:
            self._dsscontent = file.read().splitlines()

        self.__path = path
        self.__folder = pathfunc.split(path)[0]
        self.__dss_file = pathfunc.split(path)[1]
        self.__kV = kV
        self.__loadmult = loadmult
        self.init_sys()
        self.__name = self.dss.Circuit.Name()

    @property
    def dss(cls):
        """
        The instance of [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py).

        """  # noqa: E501

        return cls.opendssdirect

    @property
    def dsscontent(self) -> List[str]:
        """
        The OpenDSS commands of the ```.dss``` file in [path][dssdata.SystemClass.path].

        As well, you can change the list of commands.

        Returns:
            OpenDSS commands.
        """  # noqa: E501
        return self._dsscontent

    @dsscontent.setter
    def dsscontent(self, content: List[str]):
        self._dsscontent = content

    @property
    def name(self) -> str:
        """
        Returns:
            The name of the distribution system.
        """  # noqa: E501
        return self.__name

    @property
    def path(self) -> str:
        """
        Returns:
            The path of the ```.dss``` file.
        """  # noqa: E501
        return self.__path

    @property
    def kV(self) -> Iterable[float]:
        """
        Returns:
            The base voltages. See ```voltagebases``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf).
        """  # noqa: E501
        return self.__kV

    @property
    def loadmult(self) -> float:
        """
        Returns:
            The load multiplier.  See ```loadmult``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/> OpenDSSManual.pdf)..
        """  # noqa: E501
        return self.__loadmult

    def run_command(self, cmd: str) -> None:
        """
        Run a comand on OpenDSS.

        Args:
            cmd (str): A OpenDSS command.

        Raises:
            Exception: If the command is invalid.
        """  # noqa: E501

        self.dss.run_command(cmd)
        error = self.error
        if error != "":
            raise Exception(error)

    def cfg_system(self) -> None:
        """
        Configure the base voltages and load multiplier
        """

        self.run_command(f"Set voltagebases={self.__kV}")
        self.run_command("calcv")
        self.run_command(f"Set loadmult = {self.__loadmult}")

    def init_sys(self) -> None:
        """
        Run the commands in [dsscontent][dssdata.SystemClass.dsscontent].
        """
        directory = getcwd()
        self.dss.Basic.ClearAll()
        if self.__folder != "":
            chdir(self.__folder)
            list(map(self.run_command, self.dsscontent,))
            chdir(directory)
        else:
            list(map(self.run_command, self.dsscontent,))
        self.cfg_system()

    @property
    def error(cls) -> str:
        """
        Returns:
            The error of the last OpenDSS command.
        """
        return cls.dss.Error.Description()

    @_pf
    def get_all_bus_names(self) -> List[str]:
        """
        Returns:
            All bus names of the distribution systems.
        """
        return self.dss.Circuit.AllBusNames()

    @_pf
    def get_all_lines_names(self) -> List[str]:
        """
        Returns:
            All line names of the distribution systems.
        """
        return self.dss.Lines.AllNames()

    @_pf
    def get_all_regs_names(self) -> List[str]:
        """
        Returns:
            All regulator names of the distribution systems.
        """
        return self.dss.RegControls.AllNames()
