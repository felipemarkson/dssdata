# Development of the DSSData

## How the project is organized

The [SystemClass](https://felipemarkson.github.io/dssdata/tutorial/#loading-your-dss-file) has only the responsibility to process the ```.dss``` file.

The [Power flow modes](https://felipemarkson.github.io/dssdata/tutorial/#run-power-flow) has only the responsibility to configure and run a power flow mode with Actions and Tools.

The [Actions](https://felipemarkson.github.io/dssdata/tutorial/#creating-your-first-action) has only the responsibility to change the distribution system state temporarily.

The [Tools](https://felipemarkson.github.io/dssdata/tutorial/#creating-your-first-tool) has only the responsibility to get data information from the current state of the distribution system.

The [Reduction](https://felipemarkson.github.io/dssdata/tutorial/#creating-your-first-reduction) has only the responsibility to transform various tool's returns in a DataFrame.

See the package [documentation](https://felipemarkson.github.io/dssdata/) for more details

## The dependence manager and development environment

We use [Poetry](https://python-poetry.org/) to manage the dependencies.

You can quickly get all the development environment run the following commands:
``` bash
$ git clone https://github.com/felipemarkson/dssdata.git
$ cd dssdata
$ poetry install
$ poetry shell
```
**_Make sure that you have installed the [Python version required](https://felipemarkson.github.io/dssdata/#requirements)._**

## Linting
[Flake8](https://flake8.pycqa.org/en/latest/) in default configuration.

## Documentation

We use [Google's Style Guide](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings documentation.

All public functions must be documented at last with docstrings. 

You can see more details to how to simulate the documentation on #72.

### How to run the documentation

```console
$ mkdocs serve
```

### How to deploy the documentation
```console
$ mkdocs gh-deploy
```

## Tests and CI

We use the [unittest](https://docs.python.org/3/library/unittest.html) for our functional tests. We know that it is not the best choice, but it works fine. 

```console
$ python -m unittest
```

If you have other suggestions on how to build our tests, please tell us in an Issue.

