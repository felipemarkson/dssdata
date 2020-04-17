import opendssdirect as dss

path = "test/syste_test_IEEE13bus_timeSeries/IEEE13Nodeckt.dss"

dss.run_command(f"Compile {path}")
dss.run_command("Set Voltagebases=[115, 4.16, .48]")
dss.run_command("calcv")
dss.run_command("set mode=daily stepsize=5m hour = 0")
dss.Solution.Solve()
dss.run_command("Show Voltages LN Nodes")
dss.run_command("Show Losses")
dss.run_command("Show Currents")
