'''
Arquivo: conftest.py 
Descrição: Configura o caminho das pastas "principal" e "web" para o pytest
encontrar os módulos, não importa de onde o pytest for chamado.
'''

# Importa módulos do sistema e o pytest para configuração de caminhos e fixtures
import os
import sys

import pytest

# Obtém o diretório raiz do projeto e inclui as pastas principais no sys.path para permitir importações diretas
raiz = os.path.dirname(os.path.abspath(__file__))

for pasta in reversed([raiz, os.path.join(raiz, "principal"), os.path.join(raiz, "web")]):
    if pasta not in sys.path:
        sys.path.insert(0, pasta)


# Fixture executada automaticamente antes e depois de cada teste para limpar a instância Singleton do Banco
@pytest.fixture(autouse=True)
def resetar_banco():
    from banco import Banco
    Banco._instancia = None
    yield
    Banco._instancia = None


# Fixture que fornece uma instância padrão de Cliente válido para uso nos testes
@pytest.fixture
def cliente_exemplo():
    from cliente import Cliente
    return Cliente(
        nome="Alice Barreto Costa",
        cpf="529.982.247-25",
        data_nascimento="1995-05-15",
        email="abc@gmail.com",
        telefone="79999123456",
        endereco="Rua Secundária, 456. Bairro, Aracaju, Sergipe.",
    )


# Fixture que fornece uma instância padrão de Agencia para uso nos testes
@pytest.fixture
def agencia_exemplo():
    from agencia import Agencia
    return Agencia(
        numero_agencia="0001",
        nome="Sede",
        telefone="1111-2222",
        endereco="Rua Principal, 123. Centro, Aracaju, Sergipe.",
    )
