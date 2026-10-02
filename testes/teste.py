# Importa as bibliotecas necessárias para os testes
import pytest
import sys
import os

# Adiciona o diretório mãe ao sys.path para permitir a importação do módulo conta.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa as funções do módulo conta.py que serão testadas
from principal.conta import cadastrar_conta, depositar, sacar

# Função fixture para criar um banco com uma conta de teste
@pytest.fixture
def banco():
    contas = []
    # Cria uma conta de teste
    cadastrar_conta(contas, "12345", ("11122233344",), "001")
    return contas

# Função de teste para verificar se o depósito com valor positivo aumenta o saldo corretamente
def teste_deposito(banco):
    depositar(banco, "12345", 200.0)
    assert banco[0]["saldo"] == 200.0

# Função de teste para verificar se o saque com valor menor ou igual ao saldo diminui o saldo corretamente
def teste_saque(banco):
    depositar(banco, "12345", 200.0)
    sacar(banco, "12345", 150.0)
    assert banco[0]["saldo"] == 50.0