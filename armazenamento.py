import json

def salvar_dados(clientes, contas):
    dados_completos = [clientes, contas]
    arquivo = open("banco.json", "w")
    json.dump(dados_completos, arquivo)
    arquivo.close()