## Static Power Flow (Snapshot)

```python
from openDSSData import SystemClass
from openDSSData.pf_modes import run_static_pf
from openDSSData.tools import lines, voltages


distSys = SystemClass(path="master.dss", kV=13.8, loadmult=1.2)

run_static_pf(distSys)

lineDataFrame = lines.get_all_infos(distSys)
voltageDataFrame = voltages.get_all(distSys)

```

## Time series Power Flow

```python
from openDSSData import SystemClass
from openDSSData.pf_modes import cfg_tspf, build_dataset_tspf
from openDSSData.tools import lines, voltages


distSys = SystemClass(path="master.dss", kV=13.8, loadmult=1.2)

cfg_tspf(distSys, step_size="5m", initial_time=(0, 0))

funcs = [lines.get_all_infos, voltages.get_all]

[voltageDataFrame, lineDataFrame] = build_dataset_tspf(
    distSys, funcs_list=funcs, num_steps=288
)

```


