'''
Teste de unidade para o módulo "cliente" do pacote "principal"
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém testes de unidade para as funções do módulo "cliente.py", incluindo cadastro e busca de clientes por CPF.
'''

# Importa os módulos necessários para os testes
from principal.cliente import cadastrar_cliente, procurar_cliente

# Testa o cadastro de um cliente com CPF válido
def test_cadastrar_cliente_com_cpf_valido():
    clientes = []

    resultado = cadastrar_cliente(
        clientes, "Murilo", "529.982.247-25",
        "01/01/2000", "murilo@email.com",
        "79999999999", "Aracaju"
    )

    assert resultado == True
    assert len(clientes) == 1

# Testa o cadastro de um cliente com CPF inválido
def test_nao_cadastrar_cliente_com_cpf_invalido():
    clientes = []

    resultado = cadastrar_cliente(
        clientes, "Murilo", "111.111.111-11",
        "01/01/2000", "murilo@email.com",
        "79999999999", "Aracaju"
    )

    assert resultado == False
    assert len(clientes) == 0

# Testa a busca com CPF sem pontuação
def test_buscar_cpf_sem_pontuacao():
    clientes = []

    cadastrar_cliente(
        clientes, "Murilo", "529.982.247-25",
        "01/01/2000", "murilo@email.com",
        "79999999999", "Aracaju"
    )

    resultado = procurar_cliente(clientes, "52998224725")

    assert resultado != False
    assert resultado["nome"] == "Murilo"


# Testa a busca com CPF com pontuação
def test_buscar_cpf_com_pontuacao():
    clientes = []

    cadastrar_cliente(
        clientes, "Murilo", "52998224725",
        "01/01/2000", "murilo@email.com",
        "79999999999", "Aracaju"
    )

    resultado = procurar_cliente(clientes, "529.982.247-25")

    assert resultado != False
    assert resultado["nome"] == "Murilo"