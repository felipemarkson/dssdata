# DSSData


A python micro-framework for simulation and data analysis of electrical distribution systems modeled on [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).

Mode support: Static and Time-series


## Documentation

See [DSSData Documentation](https://felipemarkson.github.io/power-flow-analysis/).

## Installation

We strongly recommend the use of virtual environments manager.


### Using pip

```console
pip install git+https://github.com/felipemarkson/power-flow-analysis
```

### Using poetry

```console
poetry add git+https://github.com/felipemarkson/power-flow-analysis
```

Contributors: 

- [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)

<!--
### ```powerflow.losses_tools.get_total_pd_elements_losses(powerflow.systemclass.SystemClass)```

Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados do somatório das perdas de todos os elementos do tipo PD (Power Delivery). Apresenta as perdas ativas(kW) e reativas(kVAr). Ex:

|         name       |  kw_losses_total  | kvar_losses_total |
|--------------------|-------------------|-------------------|
|   all_pd_elements  |       112.398     |      327.926      |

Obs: Apesar dos capacitores serem tratados como um elemento do tipo PD, eles não são considerados.


### ```powerflow.losses_tools.get_transformer_losses(powerflow.systemclass.SystemClass)```
Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados referentes as perdas um a um dos transformadores conectaods à rede. Além disso, é apresentado o valor referente as perdas totais relacionadas aos transformadores. Apresenta as perdas ativas(kW) e reativas(kVAr).

### ```powerflow.losses_tools.get_all_pd_elements_losses(powerflow.systemclass.SystemClass)```
Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados referentes as perdas um a um dos elementos do tipo PD conectaods à rede. Apresenta as perdas ativas(kW) e reativas(kVAr).

Obs: Apesar dos capacitores serem tratados como um elemento do tipo PD, eles não são considerados.


## Como contribuir

Esteja livre para criar outras classes além do PowerFlow.

Todos atributos das classes devem ser privados, ou seja, iniciar com __ (dois underlines). Com exceção dos atributos que dão acesso ao [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py)

O acesso ou mudança de um atributo deve ser feita por um método público.

Deve-se definir quais métodos devem ser públicos e quais devem ser privados.

Os métodos privados devem iniciar com __ (dois underlines).

Dê preferência por criar funções (métodos) pequenas que possuem apenas uma única responsabilidade.

Os nomes dos atributos e dos métodos devem ser claros e legíveis, não precisa economizar no tamanho do nome ;).

Envie commits pequenos com poucas alterações por vez.


## Requisitos para Desenvolvimento

[Poetry](https://python-poetry.org/)

-->
