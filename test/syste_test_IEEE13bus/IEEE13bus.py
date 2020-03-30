import opendssdirect as dss


dss.run_command("Compile test/syste_test_IEEE13bus/IEEE13Nodeckt.dss")
dss.run_command("Set Voltagebases=[115, 4.16, .48]")
dss.run_command("calcv")
dss.Solution.Solve()
dss.run_command("Show Voltages LN Nodes")