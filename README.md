# Power flow analysis

Um módulo para organização e análises dos dados em regime permanente de sistemas de distribuição de energia elétrica utilizando como base o [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).
No momento, executa apenas o fluxo de potência estático e retorna apenas a informação de tensão.

## Requisitos

[Python 3](https://www.python.org/)


## Instalação

Realize o clone do repositório e execute o seguinte comando na pasta:

    $ pip3 install -r requirements.txt

## Uso básico

```python
from PowerFlow import PowerFlow

path_of_system = 'sua_pasta/seu_sistema.dss'

distSys = PowerFlow(path = path_of_system, kV = 13.8, loadmult = 1.2)

distSys.run_power_flow()

dataFrame = distSys.get_all_v_pu_angle_pandas()
```

## Documentação

### ```PowerFlow(path:str , kV:float/list, loadmult:float = 1)```
Define o classe para análise.

  ```path```: Caminho para o arquivo .dss com todos os dados do sistema de distribuição no padrão [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).
  Este arquivo não deve ter nenhum tipo de comando Solve.
  
  ```kV```: Valor da tensão de base para soluções em valores por unidade. Aceita uma lista de valores para sistemas de distribuição com mais de uma tensão de base.
  
  ```loadmult```: Valor em que todas as cargas do sistema serão multiplicadas. 

#### ```PowerFlow.dss```
Instância do [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py) para acesso direto da API.
    
#### ```PowerFlow.get_path()```
Retorna o caminho do arquivo.
    
#### ```PowerFlow.get_kV()```
Retorna o valor da tensão de base em kilovolts.
    
#### ```PowerFlow.get_loadmult()```
Retorna  o valor de loadmult.

#### ```PowerFlow.run_power_flow()```
Executa o fluxo de potência. Deve ser executado antes de qualquer método.

#### ```PowerFlow.get_erros()```
Retorna algum erro encontrado na resolução do fluxo de potência.

#### ```PowerFlow.get_all_bus_names()```
Retorna uma lista com todos os nomes das barras do sistema

#### ```PowerFlow.get_all_v_pu_angle_pandas()```
Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os nomes de cada barra, 
valores de tensão em pu, ângulo em graus e a configuração das fases (abc, ab, ac, bc) de todo o sistema de distribuição.

#### ```PowerFlow.get_bus_v_pu_ang_pandas(buses: list)```

   ```buses```: Lista com os nomes das barras

Retorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os nomes de cada barra, 
valores de tensão em pu, ângulo em graus e a configuração das fases (abc, ab, ac, bc).



## Como contribuir

Esteja livre para criar outras classes além do PowerFlow.

Todos atributos das classes devem ser privados, ou seja, iniciar com __ (dois underlines). Com exceção dos atributos que dão acesso ao [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py)

O acesso ou mudança de um atributo deve ser feita por um método público.

Deve-se definir quais métodos devem ser públicos e quais devem ser privados.

Os métodos privados devem iniciar com __ (dois underlines).

Dê preferência por criar funções (métodos) pequenas que possuem apenas uma única responsabilidade.

Os nomes dos atributos e dos métodos devem ser claros e legíveis, não precisa economizar no tamanho do nome ;).

Envie commits pequenos com poucas alterações por vez.

## To do

- ~Método para obter a tensão, ângulo e fases em apenas uma barra ou barras selecionadas do sistema~. 

- Método para obter as perdas totais do sistema.

- Método para obter as perdas de linhas do sistema.

- Método para obter porcentagem de carregamento das linhas.

- Método para obter a quantidade de chaveamento dos reguladores.

- Desenvolver análise de fluxo de potência temporal.

## Requisitos para Desenvolvimento

[Poetry](https://python-poetry.org/)


Contribuidor: [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)
