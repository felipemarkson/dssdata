# Power flow analysis

Um módulo para organização e análises dos dados em regime permanente de sistemas de distribuição de energia elétrica utilizando como base o [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).

Suporta os modos: Estáticos e Time series

## Requisitos

[Python 3](https://www.python.org/)


## Instalação

Realize o clone do repositório e execute o seguinte comando na pasta:

    $ pip install -r requirements.txt

## Uso básico

### Fluxo de potência: Estático

```python
from powerflow import SystemClass
from powerflow.pf_modes import run_static_pf
from powerflow.tools import lines, voltages


path_of_system = "sua_pasta/seu_sistema_sem_solve.dss"

distSys = SystemClass(path=path_of_system, kV=13.8, loadmult=1.2)

run_static_pf(distSys)

lineDataFrame = lines.get_all_infos(distSys)
voltageDataFrame = voltages.get_all(distSys)

```

### Fluxo de potência: Time series

```python
from powerflow import SystemClass
from powerflow.pf_modes import cfg_tspf, build_dataset_tspf
from powerflow.tools import lines, voltages

path_of_system = "sua_pasta/seu_sistema_sem_solve.dss"

distSys = SystemClass(path=path_of_system, kV=13.8, loadmult=1.2)

cfg_tspf(distSys, step_size="5m", initial_time=(0, 0))

funcs = (lines.get_all_infos, voltages.get_all)

[voltageDataFrame, lineDataFrame] = build_dataset_tspf(
    distSys, funcs_list=funcs, num_steps=288
)

```

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


Contribuidor: [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)
