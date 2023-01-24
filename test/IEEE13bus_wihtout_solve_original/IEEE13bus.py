import opendssdirect as dss

dss.run_command("Set Editor=nano")
dss.run_command("Compile test/IEEE13bus_wihtout_solve_original/IEEE13Nodeckt.dss")
dss.run_command("Set Voltagebases=[115, 4.16, .48]")
dss.run_command("calcv")
dss.Solution.Solve()
dss.run_command("Show Voltages LN Nodes")
dss.run_command("Show Losses")
dss.run_command("Show Currents Elements")
