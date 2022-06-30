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

## Documentation

See [DSSData Documentation](https://felipemarkson.github.io/dssdata).

## Installation

We strongly recommend the use of virtual environments manager.

### Using pip

```console
pip install dssdata
```

### Using poetry

```console
poetry add dssdata
```

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

See our [Issue](https://github.com/felipemarkson/dssdata/issues) section!


## Contributors: 

- [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)
