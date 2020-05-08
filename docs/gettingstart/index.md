
## Installation

We strongly recommend the use of virtual environments manager.


### Using pip

<div id="termynal" data-termynal>
    <span data-ty="input">pip install git+https://github.com/felipemarkson/power-flow-analysis</span>
</div>


### Using poetry

<div id="termynal" data-termynal>
    <span data-ty="input">poetry add git+https://github.com/felipemarkson/power-flow-analysis</span>
</div>

## Samples

### Static Power Flow (Snapshot)

Instance the class [```SystemClass```](api/#dssdata.SystemClass) indicating the path to the ```.dss``` file and the base system voltage.

Execute a static power flow using [```run_static_pf```](#dssdata.pfmodes.run_static_pf), informing the instance of [```SystemClass```](api/#dssdata.SystemClass) and a [```Tool```](tutorial/#creating-your-first-tool). The DSSData provides some [tools](api/#dssdata.tools) to a quick start. 

```python
from dssdata import SystemClass
from dssdata.pfmodes import run_static_pf
from dssdata.tools import voltages


distSys = SystemClass(path="master.dss", kV=[13.8], loadmult=1.2)

[voltageDataFrame] = run_static_pf(distSys, tools=[voltages.get_all])
```

### Time series Power Flow

Instance the class [```SystemClass```](api/#dssdata.SystemClass) indicating the path to the ```.dss``` file and the base system voltage.

Execute a time series power flow using [```cfg_tspf```](#dssdata.pfmodes.cfg_tspf) and [```run_tspf```](#dssdata.pfmodes.run_tspf), informing the instance of [```SystemClass```](api/#dssdata.SystemClass) and a [```Tool```](tutorial/#creating-your-first-tool). The DSSData provides some [tools](api/#dssdata.tools) to a quick start. 

```python
from dssdata import SystemClass
from dssdata.pfmodes import cfg_tspf, run_tspf
from dssdata.tools import lines, voltages


distSys = SystemClass(path="master.dss", kV=[13.8], loadmult=1.2)

cfg_tspf(distSys, step_size="5m", initial_time=(0, 0))

tools = [voltages.get_all]

[voltageDataFrame] = run_tspf(distSys, tools=tools, num_steps=288)
```
