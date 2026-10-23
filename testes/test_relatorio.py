'''
Teste de unidade para o módulo "relatorio" do pacote "principal"
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém testes de unidade para as funções do módulo "relatorio.py", incluindo cálculo do montante total, montante por agência, agência com mais clientes, quantidade de contas conjuntas, contas com saldo positivo, maior saldo, menor saldo e saldo médio.
'''

import sys # Importa o módulo sys para manipulação do caminho do sistema
import os # Importa o módulo os para manipulação de caminhos e arquivos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Adiciona a pasta raiz ao sys.path para permitir a importação do pacote "principal"
from principal.relatorio import (
    montante_total_banco, montante_por_agencia, agencia_mais_clientes, contar_contas_conjuntas,
    contas_com_saldo_positivo, conta_maior_saldo, conta_menor_saldo, saldo_medio
)


# Cria uma lista de contas (dicionários) para os testes
def criar_banco():
    return [
        {"numero": "1", "clientes": ["111"], "agencia": "0001", "saldo": 100.0},
        {"numero": "2", "clientes": ["222", "333"], "agencia": "0002", "saldo": 50.0},
        {"numero": "3", "clientes": ["111"], "agencia": "0002", "saldo": 25.0}
    ]

# Cria uma lista de contas com saldo negativo e zerado, para os testes de saldo
def criar_banco_com_negativo():
    return [
        {"numero": "1", "clientes": ["111"], "agencia": "0001", "saldo": -45.0},
        {"numero": "2", "clientes": ["222"], "agencia": "0002", "saldo": 5025.0},
        {"numero": "3", "clientes": ["333"], "agencia": "0003", "saldo": 0.0}
    ]

# Função de teste para verificar o cálculo do montante total do banco
def test_montante_total():
    assert montante_total_banco(criar_banco()) == 175.0

# Função de teste para verificar o montante total de um banco sem contas
def test_montante_total_sem_contas():
    assert montante_total_banco([]) == 0.0

# Função de teste para verificar o cálculo do montante por agência
def test_montante_por_agencia():
    assert montante_por_agencia(criar_banco(), "0002") == 75.0

# Função de teste para verificar a agência com mais clientes
def test_agencia_mais_clientes():
    assert agencia_mais_clientes(criar_banco()) == "0002"

# Função de teste para verificar a agência com mais clientes quando não há contas
def test_agencia_mais_clientes_sem_contas():
    assert agencia_mais_clientes([]) == False

# Função de teste para verificar a contagem de contas conjuntas
def test_contas_conjuntas():
    assert contar_contas_conjuntas(criar_banco()) == 1

# Função de teste para verificar que só entram contas com saldo maior que zero
def test_contas_com_saldo_positivo():
    positivas = contas_com_saldo_positivo(criar_banco_com_negativo())
    assert len(positivas) == 1
    assert positivas[0]["numero"] == "2"

# Função de teste para verificar que saldo zero não conta como positivo
def test_contas_com_saldo_positivo_ignora_zero():
    assert contas_com_saldo_positivo([{"numero": "1", "saldo": 0.0}]) == []

# Função de teste para verificar a conta com o maior saldo
def test_conta_maior_saldo():
    assert conta_maior_saldo(criar_banco_com_negativo())["numero"] == "2"

# Função de teste para verificar a conta com o menor saldo (saldo negativo)
def test_conta_menor_saldo():
    assert conta_menor_saldo(criar_banco_com_negativo())["numero"] == "1"

# Função de teste para verificar que maior e menor saldo devolvem dicionário vazio sem contas
def test_maior_e_menor_saldo_sem_contas():
    assert conta_maior_saldo([]) == {}
    assert conta_menor_saldo([]) == {}

# Função de teste para verificar o saldo médio das contas
def test_saldo_medio():
    assert saldo_medio(criar_banco()) == 175.0 / 3

# Função de teste para verificar o saldo médio de um banco sem contas
def test_saldo_medio_sem_contas():
    assert saldo_medio([]) == 0.0