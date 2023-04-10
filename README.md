# DSSData

[![PyPI version](https://badge.fury.io/py/dssdata.svg)](https://pypi.org/project/dssdata/)
[![DOI](https://zenodo.org/badge/250637349.svg)](https://zenodo.org/badge/latestdoi/250637349)
[![License](https://img.shields.io/github/license/felipemarkson/dssdata)](https://github.com/felipemarkson/dssdata/blob/master/LICENSE)

![Tests](https://github.com/felipemarkson/dssdata/actions/workflows/test.yml/badge.svg)
[![PyPI Downloads](https://img.shields.io/pypi/dm/dssdata.svg?label=PyPI%20downloads)](
https://pypi.org/project/dssdata/)
![stars](https://img.shields.io/github/stars/felipemarkson/dssdata)

_**⚡A python micro-framework for steady-state simulation and data analysis of electrical distribution systems modeled on [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).**_

Mode support: Static and Time-series.

## Why DSSData?
The purpose of DSSData is to facilitate the steady-state simulation of modern electrical distribution systems, such as microgrids, smart grids, and smart cities.

With DSSData you can easily make your own super new fancy operation strategies with storage or generators, probabilistic simulation, or simple impact studies of a distributed generator. See an example in our [Tutorial](https://felipemarkson.github.io/dssdata/tutorial/).

**_All you need is your base distribution system modeled in OpenDSS!!!_**

### Easy to simulate

We built the DSSData for you just write what you want in a simple function, plugin on a power flow mode, and run. 

You don't need anymore write a routine to run each power flow per time. 

## Quick Start
### Installation

We strongly recommend the use of virtual environments manager.

```console
pip install dssdata
```

### Static Power Flow (Snapshot)

First, comment any `solve`, output command (e.g: `show`), or solve configurations (e.g: `set mode=Snap`) from your `.dss` file.

_**NOTE**: Any `Monitor` is needed to get the data._

Supposing that you file is in the path `master.dss`:

```python
from dssdata import SystemClass
from dssdata.pfmodes import run_static_pf
from dssdata.tools import voltages

distSys = SystemClass(path="master.dss", kV=[13.8, 0.230], loadmult=1.0)

[voltageDataFrame] = run_static_pf(distSys, tools=[voltages.get_all])
print(voltageDataFrame)
```

### Time series Power Flow

First, comment any `solve`, output command (e.g: `show`), or solve configurations (e.g: `set mode=daily stepsize=5m time=...`) from your `.dss` file.

_**NOTE**: Any `Monitor` is needed to get the data._

_**NOTE**: The `Loadshape` must be defined in the `.dss` file_

Supposing that you file is in the path `master.dss`:

```python
from dssdata import SystemClass
from dssdata.pfmodes import cfg_tspf, run_tspf
from dssdata.tools import lines, voltages

distSys = SystemClass(path="master.dss", kV=[13.8], loadmult=1.2)
cfg_tspf(distSys, step_size="5m", initial_time=(0, 0))

[voltageDataFrame] = run_tspf(distSys, tools=[voltages.get_all], num_steps=288)
print(voltageDataFrame)
```

## Documentation

We provide an full API documentation and examples in the [DSSData Documentation](https://felipemarkson.github.io/dssdata).

## Citing

If you find DSSData useful in your work, we kindly request that you cite it as below: 
```bibtex
@software{Monteiro_felipemarkson_dssdata_v0_1_7_2022,
  author = {Monteiro, Felipe},
  doi = {10.5281/zenodo.6784238},
  license = {MIT},
  month = {6},
  title = {{felipemarkson/dssdata: v0.1.7}},
  url = {https://github.com/felipemarkson/dssdata},
  version = {0.1.7},
  year = {2022}
}
```

## Help us to improve DSSData

See our [Issue](https://github.com/felipemarkson/dssdata/issues) section, our [Development Guidelines](DEV.md), and our [Code of conduct](CODE_OF_CONDUCT.md).

### Contributors: 

- [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)
