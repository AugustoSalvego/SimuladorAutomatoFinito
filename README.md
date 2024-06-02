 ## Simulador de autômato finito

Projeto de um simulador de autômato finito na linguagem python.


## Funcionalidades

- Leitura de autômatos a partir de arquivos JSON.
- Leitura de palavras a serem testadas a partir de arquivos CSV.
- Identificação automática do tipo de autômato (DFA ou NFA).
- Simulação de autômatos finitos com e sem epsilon-transições.
- Geração de resultados de simulação em arquivos CSV, incluindo o tempo de processamento.

## Estrutura dos Arquivos

    Para usar o simulador é necessário três arquivos.
    
### Arquivo JSON 

O arquivo JSON deve conter os seguintes campos:

- `initial`: Estado inicial.
- `final`: Lista de estados de aceitação.
- `transitions`: Lista de transições, onde cada transição é um objeto com os campos `from`, `read` (pode ser `null` para epsilon-transições), e `to`.

### Exemplo de arquivo JSON
    
    {
      "initial": 0,
      "final": [2],
      "transitions": [
        { 
          "from": "0",
          "to": "0",
          "read": "a" 
        },
        { 
          "from": "2",
          "to": "2",
          "read": "a" 
        },
        { 
          "from": "1",
          "to": "1",
          "read": "b" 
        },
        { 
          "from": "1",
          "to": "2",
          "read": "a" 
        },
        { 
          "from": "0",
          "to": "1",
          "read": "b" 
        }
      ]
    }
   
### Arquivo CSV

CSV de Palavras:
    O arquivo CSV deve conter as palavras a serem testadas e o resultado esperado (1 para aceitação, 0 para rejeição), separados por ponto e vírgula (;).

### Exemplo de arquivo csv

    ba;1
    aaaabbbbbaaaaa;1
    abababab;0
    bbbbbbbb;0
    aaaaaaaaaaaa;0
    aaaaabaaaaa;1
    
### Como usar no terminal

Usando o terminal abra a pasta

    cd Trabalho simulador
    
Utilize os comandos
        
    python SimuladorAutomatoFinito.py
    ex1json.txt 
    ex1csv.txt 
    saida1.txt
 

### O Código irá realizar a saída em um arquivo CSV
    
   O formato será:
   
    palavra; resultado esperado; resultado obtido; tempo em segundos
    
### Exemplo de saída CSV 

    ba;1;1;0.0011483
    aaaabbbbbaaaaa;1;1;7.12e-05
    abababab;0;0;1.65e-05
    bbbbbbbb;0;0;2.26e-05
    aaaaaaaaaaaa;0;0;3.11e-05
    aaaaabaaaaa;1;1;2.91e-05
