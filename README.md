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


path_of_system = 'sua_pasta/seu_sistema_sem_solve.dss'

distSys = SystemClass(path = path_of_system, kV = 13.8, loadmult = 1.2)

run_static_pf(distSys)

lineDataFrame = line.get_all_infos(distSys)
voltageDataFrame = voltages.get_all(distSys)
```

### Fluxo de potência: Time series

```python
from powerflow import SystemClass
from powerflow.pf_modes import cfg_tspf, build_dataset_tspf
from powerflow.tools import lines, voltages

path_of_system = 'sua_pasta/seu_sistema_sem_solve.dss'

distSys = SystemClass(path = path_of_system, kV = 13.8, loadmult = 1.2)

cfg_tspf(distSys, step_size = '5m', initial_time = (0,0))

funcs = (line.get_all_infos, voltages.get_all)

[voltageDataFrame, lineDataFrame] = buil_dataset_tspf(
                                      distSys, 
                                      funcs_list = funcs, 
                                      num_steps = 288
                                    )

```
<!--
## Documentação

### ```powerflow.systemclass.SystemClass(path:str , kV:float/list, loadmult:float = 1)```
Define a classe para análise.

  ```path```: Caminho para o arquivo .dss com todos os dados do sistema de distribuição no padrão [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).
  Este arquivo não deve ter nenhum tipo de comando Solve.
  
  ```kV```: Valor da tensão de base para soluções em valores por unidade. Aceita uma lista de valores para sistemas de distribuição com mais de uma tensão de base.
  
  ```loadmult```: Valor em que todas as cargas do sistema serão multiplicadas. 

#### ```powerflow.systemclass.SystemClass.dss ```
Instância do [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py) para acesso direto a API.
    
#### ```powerflow.systemclass.SystemClass.get_name()```
Retorna o nome do circuito.

#### ```powerflow.systemclass.SystemClass.get_path()```
Retorna o caminho do arquivo.
    
#### ```powerflow.systemclass.SystemClass.get_kV()```
Retorna o valor da tensão de base em kilovolts.
    
#### ```powerflow.systemclass.SystemClass.get_loadmult()```
Retorna  o valor de loadmult.

#### ```powerflow.systemclass.SystemClass.compile()```
Configura o sistema para o [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py).


#### ```powerflow.systemclass.SystemClass.get_all_bus_names()```
Retorna uma lista com todos os nomes das barras do sistema

#### ```powerflow.systemclass.SystemClass.get_all_lines_names()```
Retorna uma lista com todos os nomes das linhas do sistema

### ```powerflow.voltage_tools.get_all_v_pu_ang(powerflow.SystemClass)```
Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com as informações de tensão de todas as barras. Ex:

|    | bus_name | v_pu_a  | v_pu_b  | v_pu_c  | ang_a | ang_b  | ang_c | phases |
|----|-----------|---------|---------|---------|-------|--------|-------|--------|
| 0  | sourcebus | 0.99997 | 0.99999 | 0.99995 | 30.0  | -90.0  | 150.0 | abc    |
| 1  | 646       |   NaN      | 1.01803 | 1.00026 |   NaN    | -122.0 | 117.8 | bc     |
| 2 | 611       |    NaN     |    NaN     | 0.96083 |   NaN    |    NaN    | 115.7 | c      |
| 3 | 652       | 0.97533 |    NaN     |   NaN      | -5.3  |    NaN    |  NaN     | a      |

### ```powerflow.voltage_tools.get_bus_v_pu_ang(powerflow.systemclass.SystemClass, buses: list)```
```buses```: Lista com os nomes das barras.

Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com as informações de tensão das barras na lista.


#### ```powerflow.line_tools.get_all_line_infos(powerflow.systemclass.SystemClass)```
Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados das linhas de todo o sistema de distribuição. Ex:

|    | name   | bus1 | ph_bus1 | bus2 | ph_bus2 | I(A)_bus1_ph_a | I(A)_bus1_ph_b | I(A)_bus1_ph_c | I(A)_bus2_ph_a | I(A)_bus2_ph_b | I(A)_bus2_ph_c | ang_bus1_ph_a | ang_bus1_ph_b | ang_bus1_ph_c | ang_bus2_ph_a | ang_bus2_ph_b | ang_bus2_ph_c | kw_losses | kvar_losses | emergAmps | normAmps | perc_NormAmps | perc_EmergAmps |
|----|--------|------|---------|------|---------|----------------|----------------|----------------|----------------|----------------|----------------|---------------|---------------|---------------|---------------|---------------|---------------|-----------|-------------|-----------|----------|---------------|----------------|
| 0  | 650632 | rg60 | abc     | 632  | abc     | 562.609        | 419.029        | 591.793        | 562.61         | 419.03         | 591.794        | -28.7         | -141.3        | 93.4          | 151.3         | 38.7          | -86.6         | 60.737    | 196.015     | 600.0     | 400.0    | 1.479         | 0.986          |
| 1  | 632670 | 632  | abc     | 670  | abc     | 481.916        | 218.055        | 480.313        | 481.916        | 218.055        | 480.313        | -27.2         | -135.2        | 99.6          | 152.8         | 44.8          | -80.4         | 12.991    | 41.495      | 600.0     | 400.0    | 1.205         | 0.803          |
| 2  | 670671 | 670  | abc     | 671  | abc     | 473.795        | 188.824        | 424.942        | 473.795        | 188.824        | 424.942        | -27.0         | -132.6        | 101.3         | 153.0         | 47.4          | -78.7         | 22.729    | 72.334      | 600.0     | 400.0    | 1.184         | 0.79           |




#### ```powerflow.line_tools.get_line_infos(powerflow.systemclass.SystemClass, lines_names: list)```
```lines_names```: Lista com os nomes das linhas.

Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados das linhas da lista.


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

### ```powerflow.pf_modes.run_power_flow(powerflow.systemclass.SystemClass)```
Executa o fluxo de potência em modo estático.

### ```powerflow.pf_modes.cfg_tspf(powerflow.systemclass.SystemClass, step_size: '1h', initial_time: (0, 0)))```
Configura o sistema para a execução em modo time series.

```step_size```: Tamanho do passo de integração. Veja "Stepsize" em [OpenDSS User Manual](https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Distrib/Doc/OpenDSSManual.pdf?format=raw).

```initial_time```: Tupla com a hora e o segundo inicial da simulação. Veja "Time" em [OpenDSS User Manual](https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Distrib/Doc/OpenDSSManual.pdf?format=raw).

### ```powerflow.pf_modes.buil_dataset_tspf(powerflow.systemclass.SystemClass, funcs_list: list = [lambda distSys:pd.Dataframe()], num_steps: int)```
Retorna uma lista com o retorno das funções nas listas.

```funcs_list```: lista com as funções de aquisição de informação.

```num_steps```: Quantidade de passos de integração que serão realizados.
 --> 

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
