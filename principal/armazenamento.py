'''
Módulo: armazenamento.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para salvar e carregar dados do banco de dados (JSON com dicionário).
'''

# Importa o módulo json para ler e escrever estruturas de dados no formato JSON
import json

# Importa o módulo os para verificar a existência de arquivos no sistema operacional
import os

# Define o nome e caminho padrão do arquivo de armazenamento do banco
CAMINHO_PADRAO = "banco.json"


# Função para ler os dados armazenados no arquivo JSON
def ler_json(caminho: str = CAMINHO_PADRAO) -> dict:
    # Verifica se o arquivo JSON existe; caso não exista, retorna a estrutura inicial vazia
    if not os.path.exists(caminho):
        return {"agencia": None, "clientes": [], "contas": []}
    # Abre o arquivo no modo de leitura com codificação UTF-8 e converte o JSON em dicionário Python
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# Função para gravar os dados do banco no arquivo JSON
def gravar_json(dados: dict, caminho: str = CAMINHO_PADRAO) -> None:
    # Abre o arquivo no modo de escrita com codificação UTF-8 e salva o dicionário formatado
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
