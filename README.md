# Projeto Orifice Plate

Este projeto contém uma implementação de um orifício de placa para medir o fluxo de fluidos. Ele inclui uma interface de usuário gráfico para facilitar o uso.

## Execução em Linux

1. Instale as dependências listadas no arquivo `requirements.txt` com o seguinte comando:

```shell
pip install -r requirements.txt
```

2. Execute o arquivo principal `main.py` com o seguinte comando:


```shell
python3 main.py
```

## Execução em Windows

1. Instale as dependências listadas no arquivo `requirements.txt` com o seguinte comando:

```shell
pip install -r requirements.txt
```

2. Execute o arquivo principal `main.py` com o seguinte comando:

```shell
python main.py
```


## Estrutura de Diretórios

```shell
root/
|-- orifice_plate/
| |-- init.py
| |-- orifice_plate.py
|-- ui/
| |-- init.py
| |-- ui.py
|-- main.py
requirements.txt
```

## Detalhamento do código

Referências principais

Cálculo de coeficiente de descarga:

[FLUID MECHANICS](http://ftp.demec.ufpr.br/disciplinas/TM240/Marchi/Bibliografia/White_2011_7ed_Fluid-Mechanics.pdf)

Tipos de tap e posicionamento relativo ao diâmetro interno da tubulação:

[Orifice Plate Taps](https://forumautomation.com/t/orifice-plate-taps/4982)