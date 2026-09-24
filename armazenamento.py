import json
import os

def salvar_dados(clientes, agencias, contas):
    todas_as_listas = [clientes, agencias, contas]
    arquivo_banco = open("banco.json", "w")
    json.dump(todas_as_listas, arquivo_banco)
    arquivo_banco.close()

def carregar_dados():
    if os.path.exists("banco.json") == True:
        arquivo_banco = open("banco.json", "r")
        todas_as_listas = json.load(arquivo_banco)
        arquivo_banco.close()
        lista_clientes = todas_as_listas[0]
        lista_agencias = todas_as_listas[1]
        lista_contas = todas_as_listas[2]
        return lista_clientes, lista_agencias, lista_contas
    else:
        clientes_vazios = []
        agencias_vazias = []
        contas_vazias = []
        return clientes_vazios, agencias_vazias, contas_vazias