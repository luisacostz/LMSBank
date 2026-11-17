'''
Módulo: armazenamento.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para salvar e carregar dados do banco de dados (JSON com dicionário).
'''

import json # Importa a biblioteca 'json' para manipulação de arquivos JSON
import os # Importa a biblioteca 'os' para verificar a existência de arquivos

# Função para salvar os dados do banco de dados em um arquivo JSON
def salvar_dados(clientes, agencias, contas):
    # Agora o JSON é um dicionário com três listas de dicionários
    dados = {
        "clientes": clientes,
        "agencias": agencias,
        "contas": contas
    }
    # Abre o arquivo 'banco.json' em modo de escrita ('w' - write)
    arquivo_banco = open("banco.json", "w", encoding="utf-8")
    # Converte e salva o dicionário no arquivo JSON
    json.dump(dados, arquivo_banco, ensure_ascii=False, indent=4)
    # Fecha o arquivo para salvar as alterações e liberar recursos do sistema
    arquivo_banco.close()


# Função para carregar os dados do banco de dados a partir de um arquivo JSON
def carregar_dados():
    # Verifica se o arquivo 'banco.json' existe
    if os.path.exists("banco.json") == True:
        arquivo_banco = open("banco.json", "r", encoding="utf-8")
        # Carrega o dicionário do arquivo JSON
        dados = json.load(arquivo_banco)
        arquivo_banco.close()

        # Retorna as listas de clientes, agências e contas separadamente
        return dados["clientes"], dados["agencias"], dados["contas"]
    else:
        # Se o arquivo não existir, retorna listas vazias para clientes, agências e contas
        return [], [], []