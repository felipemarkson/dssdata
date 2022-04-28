from os import getcwd, chdir
from os import path as pathfunc
from typing import Iterable, List

__version__ = "0.1.6"


def _redirect_handler(path) -> List[str]:
    """
    If a redirect command is found, call the function recursively
    Args:
        path: The path to the file.
        acc: A buffer to store the commands.
    Returns:
        True if the file has a solve command.
    """
    with open(path, "rt") as file:
        lines = file.readlines()

    commands = _remove_comments_dss(lines)
    no_redirect_cmds = []

    for line in commands:
        if "redirect" in line.lower().strip():
            cmd = " ".join(line.split(" ")[1:]).strip()
            head = pathfunc.split(path)[0]
            no_redirect_cmds += _redirect_handler(pathfunc.join(head, cmd))
        else:
            no_redirect_cmds.append(line)

    return no_redirect_cmds


def _remove_comments_dss(list_cmd: List[str]) -> List[str]:

    vanished: List[str] = []
    in_a_comment = False
    for cmd in list_cmd:
        if cmd.strip().startswith("/*"):
            in_a_comment = True
            continue
        elif cmd.strip().endswith("*/"):
            in_a_comment = False
            continue
        if in_a_comment:
            continue
        elif cmd.strip().startswith("!"):
            continue
        elif cmd.strip().startswith("//"):
            continue
        elif len(cmd.strip()) == 0:
            continue

        if cmd.strip().startswith("~"):
            vanished[-1] += cmd.strip()[1:].split("!")[0]
        else:
            vanished.append(cmd.strip())

    return vanished


class SystemClass:
    """
    The distribution system abstraction class.
    """  # noqa: E501

    import opendssdirect

    def __init__(self, *, path: str, kV: Iterable[float], loadmult: float = 1):
        """
        Args:
            path (str): The path to the file that describes the distribution system.
            kV (Iterable[float]): The base voltages. See ```voltagebases``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf).
            loadmult (float, optional): The load multiplier.  See ```loadmult``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/> OpenDSSManual.pdf).
        """  # noqa: E501

        self._dsscontent = _redirect_handler(path)

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
        self.init_sys()

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
            The load multiplier.  See ```loadmult``` in [OpenDSS User Manual](http://svn.code.sf.net/p/electricdss/code/trunk/Distrib/Doc/OpenDSSManual.pdf)..
        """  # noqa: E501
        return self.__loadmult

    def run_command(self, cmd: str) -> str:
        """
        Run a comand on OpenDSS.

        Args:
            cmd (str): A OpenDSS command.

        Raises:
            Exception: If the command is invalid.
        Returns:
            The OpenDSS command returns
        """  # noqa: E501

        # value = self.dss.run_command(cmd, dss=self.dss)
        self.dss.Text.Command(cmd)
        error = self.error
        if error != "":
            raise Exception(error)

        return self.dss.Text.Result()

    def init_sys(self):
        """
        Run the commands in [dsscontent][dssdata.SystemClass.dsscontent].
        """
        directory = getcwd()
        self.dss.Basic.ClearAll()
        if self.__folder != "":
            chdir(self.__folder)
            list(
                map(
                    self.run_command,
                    self._dsscontent,
                )
            )
            chdir(directory)
        else:
            list(
                map(
                    self.run_command,
                    self._dsscontent,
                )
            )

        self.run_command(f"Set voltagebases={self.__kV}")
        self.run_command("calcv")
        self.run_command(f"Set loadmult = {self.__loadmult}")

    @property
    def error(cls) -> str:
        """
        Returns:
            The error of the last OpenDSS command.
        """
        return cls.dss.Error.Description()
