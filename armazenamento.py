'''
Módulo: armazenamento.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para salvar e carregar dados do banco de dados.
'''

import json # Importa a biblioteca 'json' para manipulação de arquivos JSON
import os # Importa a biblioteca 'os' para verificar a existência de arquivos

# Função para salvar os dados do banco de dados em um arquico JSON
def salvar_dados(clientes, agencias, contas):
    # Cria uma lista contendo todas as listas de clientes, agências e contas
    todas_as_listas = [clientes, agencias, contas]
    # Abre o arquivo 'banco.json' em modo de escrita ('w' - write) 
    arquivo_banco = open("banco.json", "w")
    # Converte e salva a lista agrupada de dados no arquivo JSON
    json.dump(todas_as_listas, arquivo_banco)
    # Fecha o arquivo para salvar as alterações e liberar recursos do sistema
    arquivo_banco.close()

# Função para carregar os dados do banco de dados a partir de um arquivo JSON
def carregar_dados():
    # Verifica se o arquivo 'banco.json' existe
    if os.path.exists("banco.json") == True:
        # Abre o arquivo 'banco.json' em modo de leitura ('r' - read) 
        arquivo_banco = open("banco.json", "r")
        # Carrega os dados do arquivo JSON e armazena na variável 'todas_as_listas'
        todas_as_listas = json.load(arquivo_banco)
        # Fecha o arquivo após a leitura
        arquivo_banco.close()

        # Retorna as listas de clientes, agências e contas separadamente
        lista_clientes = todas_as_listas[0]
        lista_agencias = todas_as_listas[1]
        lista_contas = todas_as_listas[2]
        return lista_clientes, lista_agencias, lista_contas
    else:
        # Se o arquivo não existir, retorna listas vazias para clientes, agências e contas
        clientes_vazios = []
        agencias_vazias = []
        contas_vazias = []
        return clientes_vazios, agencias_vazias, contas_vazias