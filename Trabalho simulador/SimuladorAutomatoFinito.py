import json
import csv
import time
from collections import defaultdict, deque

#Lê um arquivo JSON e retorna seu conteúdo como um dicionário.
def ler_arquivo_json(caminho):
    with open(caminho, 'r') as f:
        return json.load(f)

#Lê um arquivo CSV e retorna seu conteúdo como uma lista de tuplas.
def ler_arquivo_csv(caminho):
    with open(caminho, 'r') as f:
        leitor_csv = csv.reader(f, delimiter=';')
        entradas = [(linha[0], int(linha[1])) for linha in leitor_csv]
    return entradas

#Salva os resultados em um arquivo CSV.
def salvar_resultados(caminho, resultados):
    with open(caminho, 'w', newline='') as f:
        escritor_csv = csv.writer(f, delimiter=';')
        escritor_csv.writerows(resultados)

#Calcula o fecho épsilon de um estado em um autômato.
def epsilon_closure(estado, transicoes):
    fecho = set()
    fila = deque([estado])
    while fila:
        estado_atual = fila.popleft()
        fecho.add(estado_atual)
        chave = f'{estado_atual}'
        if chave in transicoes:
            for novo_estado in transicoes[chave]:
                if novo_estado not in fecho:
                    fila.append(novo_estado)
    return fecho

#Simula um autômato determinístico (DFA).
def simula_dfa(estado_inicial, estados_aceitacao, transicoes, palavra):
    estado_atual = estado_inicial
    for simbolo in palavra:
        chave = f'{estado_atual}{simbolo}'
        if chave in transicoes:
            estado_atual = transicoes[chave][0]  # Pega o primeiro estado da lista
            if estado_atual is None:
                return False
        else:
            return False
    return estado_atual in estados_aceitacao

#Simula um autômato não determinístico (NFA).
def simula_nfa(estado_inicial, estados_aceitacao, transicoes, palavra):
    estados_atuais = epsilon_closure(estado_inicial, transicoes)
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            chave = f'{estado}{simbolo}'
            if chave in transicoes:
                for novo_estado in transicoes[chave]:
                    novos_estados.update(epsilon_closure(novo_estado, transicoes))
        estados_atuais = novos_estados
    return any(estado in estados_atuais for estado in estados_aceitacao)

#Detecta o tipo de um autômato (DFA ou NFA).
def detecta_tipo_automato(transicoes):
    for chave, destinos in transicoes.items():
        if len(destinos) > 1:
            return 'NFA'
        if '' in chave:  # Verifica presença de transições vazias
            return 'NFA'
    return 'DFA'

#Processa um autômato a partir de um arquivo JSON e testa suas transições com base em um arquivo CSV.
def processa_automato(arquivo_json, arquivo_csv, arquivo_saida):
    
    # Carrega o autômato a partir do arquivo JSON
    data = ler_arquivo_json(arquivo_json)
    # Lê as palavras a serem testadas a partir do arquivo CSV
    entradas = ler_arquivo_csv(arquivo_csv)

    # Extrai informações do autômato do arquivo JSON
    estado_inicial = data['initial']
    estados_aceitacao = [str(estado) for estado in data['final']]
    transicoes = defaultdict(list)
    for transicao in data['transitions']:
        chave = f"{transicao['from']}{transicao.get('read', '')}"
        transicoes[chave].append(transicao['to'])
    
    # Detecta o tipo de autômato (DFA ou NFA)
    tipo_automato = detecta_tipo_automato(transicoes)
    resultados = []

    # Processa cada palavra de entrada e armazena os resultados
    for palavra, resultado_esperado in entradas:
        tempo_inicial = time.perf_counter_ns()

        # Simula o autômato com base no tipo
        if tipo_automato == 'DFA':
            resultado_obtido = simula_dfa(estado_inicial, estados_aceitacao, transicoes, palavra)
        elif tipo_automato == 'NFA':
            resultado_obtido = simula_nfa(estado_inicial, estados_aceitacao, transicoes, palavra)

        tempo_final = time.perf_counter_ns()
        tempo_decorrido = (tempo_final - tempo_inicial) / 1e9  # Tempo em segundos
        
        # Armazena os resultados (palavra, resultado_esperado, resultado_obtido, tempo_decorrido)
        resultados.append((palavra, resultado_esperado, int(resultado_obtido), tempo_decorrido))
    
    # Salva os resultados no arquivo de saída
    salvar_resultados(arquivo_saida, resultados)

def main_function():
    print("Informe o arquivo de entrada - json:", end=" ")
    file_json = input()
    print("Informe o arquivo de teste - csv:", end=" ")
    file_csv = input()
    print("Informe o arquivo de saída - csv:", end=" ")
    file_out = input()

    # Processa o autômato e salva os resultados no arquivo de saída
    processa_automato(file_json, file_csv, file_out)

if __name__ == "__main__":
    main_function()
