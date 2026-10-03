'''
Teste de unidade para o módulo "relatorio" do pacote "principal"
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém testes de unidade para as funções do módulo "relatorio.py", incluindo cálculo do montante total, montante por agência, agência com mais clientes e quantidade de contas conjuntas.
'''

import sys # Importa o módulo sys para manipulação do caminho do sistema
import os # Importa o módulo os para manipulação de caminhos e arquivos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Adiciona a pasta raiz ao sys.path para permitir a importação do pacote "principal"
from principal.relatorio import montante_total_banco, montante_por_agencia, agencia_mais_clientes, contar_contas_conjuntas


# Cria uma lista de contas (dicionários) para os testes
def criar_banco():
    return [
        {"numero": "1", "clientes": ["111"], "agencia": "0001", "saldo": 100.0},
        {"numero": "2", "clientes": ["222", "333"], "agencia": "0002", "saldo": 50.0},
        {"numero": "3", "clientes": ["111"], "agencia": "0002", "saldo": 25.0}
    ]

# Função de teste para verificar o cálculo do montante total do banco
def test_montante_total():
    assert montante_total_banco(criar_banco()) == 175.0

# Função de teste para verificar o cálculo do montante por agência
def test_montante_por_agencia():
    assert montante_por_agencia(criar_banco(), "0002") == 75.0

# Função de teste para verificar a agência com mais clientes
def test_agencia_mais_clientes():
    assert agencia_mais_clientes(criar_banco()) == "0002"

# Função de teste para verificar a contagem de contas conjuntas
def test_agencia_mais_clientes_sem_contas():
    assert agencia_mais_clientes([]) == False

# Função de teste para verificar a contagem de contas conjuntas
def test_contas_conjuntas():
    assert contar_contas_conjuntas(criar_banco()) == 1