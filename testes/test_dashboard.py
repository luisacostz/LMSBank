'''
Teste de unidade para o módulo "dashboard" da pasta "web"
Descrição: Este módulo contém testes de unidade para a função montar_dashboard, que reúne os números exibidos na página do dashboard.
'''

import sys # Importa o módulo sys para manipulação do caminho do sistema
import os # Importa o módulo os para manipulação de caminhos e arquivos

# Adiciona as pastas "principal" e "web" ao sys.path (o dashboard.py importa o módulo "relatorio")
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(raiz, 'principal'))
sys.path.append(os.path.join(raiz, 'web'))
from dashboard import montar_dashboard


# Cria os dados de exemplo para os testes
def criar_dados():
    clientes = [{"nome": "Alice", "cpf": "111"}, {"nome": "Bento", "cpf": "222"}]
    agencias = [{"numero_agencia": "0001", "nome": "Matriz"}]
    contas = [
        {"numero": "1", "clientes": ["111"], "agencia": "0001", "saldo": -45.0},
        {"numero": "2", "clientes": ["222"], "agencia": "0001", "saldo": 5025.0},
        {"numero": "3", "clientes": ["111", "222"], "agencia": "0001", "saldo": 20.0}
    ]
    return clientes, agencias, contas

# Testa as contagens de clientes, agências e contas
def test_dashboard_contagens():
    dados = montar_dashboard(*criar_dados())
    assert dados["num_clientes"] == 2
    assert dados["num_agencias"] == 1
    assert dados["num_contas"] == 3

# Testa o saldo total e o saldo médio
def test_dashboard_saldo_total_e_medio():
    dados = montar_dashboard(*criar_dados())
    assert dados["saldo_total"] == 5000.0
    assert dados["saldo_medio"] == 5000.0 / 3

# Testa o maior saldo e a conta dona dele
def test_dashboard_maior_saldo():
    dados = montar_dashboard(*criar_dados())
    assert dados["maior_saldo"] == 5025.0
    assert dados["maior_saldo_conta"] == "2"

# Testa o menor saldo e a conta dona dele
def test_dashboard_menor_saldo():
    dados = montar_dashboard(*criar_dados())
    assert dados["menor_saldo"] == -45.0
    assert dados["menor_saldo_conta"] == "1"

# Testa o dashboard de um banco vazio: tudo zerado, sem erro
def test_dashboard_banco_vazio():
    dados = montar_dashboard([], [], [])
    assert dados["num_contas"] == 0
    assert dados["saldo_total"] == 0.0
    assert dados["saldo_medio"] == 0.0
    assert dados["maior_saldo"] == 0.0
    assert dados["menor_saldo"] == 0.0
    assert dados["maior_saldo_conta"] == ""
    assert dados["menor_saldo_conta"] == ""