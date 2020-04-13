from .systemclass import SystemClass


def run_power_flow(distSys: SystemClass):
    distSys.dss.run_command("set mode=Snap")
    distSys.dss.Solution.Solve()