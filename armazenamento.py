import json

def salvar_dados(clientes, contas, agencias):
    dados_completos = [clientes, contas, agencias]
    arquivo = open("banco.json", "w")
    json.dump(dados_completos, arquivo)
    arquivo.close()
