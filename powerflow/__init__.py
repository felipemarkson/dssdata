from .systemclass import SystemClass


def run_power_flow(distSys: SystemClass):
    distSys.dss.Solution.Solve()
