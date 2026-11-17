'''
Teste de unidade para o módulo "cliente" do pacote "principal"
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém testes de unidade para as funções do módulo "cliente.py", incluindo cadastro e busca de clientes por CPF.
'''

"""
Módulo: test_cliente.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Testes automatizados para validar a criação, validação de CPF, vínculo de contas, cálculo de saldo total e serialização (JSON) da classe Cliente.
"""

# Importa o pytest, as classes de modelo e as exceções utilizadas nos testes
import pytest

from cliente import Cliente
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from excecoes import BancoError, CpfInvalidoError


# Verifica se o CPF válido com pontuação é armazenado apenas com dígitos numéricos
def test_cliente_com_cpf_valido_guarda_so_numeros():
    cliente = Cliente(nome="Murilo", cpf="529.982.247-25")
    assert cliente.cpf == "52998224725"
    assert cliente.nome == "Murilo"


# Verifica se o CPF informado sem pontuação é aceito e mantido corretamente
def test_cliente_com_cpf_sem_pontuacao():
    assert Cliente(nome="Murilo", cpf="52998224725").cpf == "52998224725"


# Testa múltiplos cenários de CPFs inválidos garantindo o lançamento de CpfInvalidoError
@pytest.mark.parametrize("cpf", ["111.111.111-11", "529.982.247-24", "123456", "5299822472A", ""])
def test_cliente_com_cpf_invalido_levanta_erro(cpf):
    with pytest.raises(CpfInvalidoError):
        Cliente(nome="Murilo", cpf=cpf)


# Verifica se CpfInvalidoError herda corretamente da exceção base BancoError
def test_cpf_invalido_e_um_banco_error():
    with pytest.raises(BancoError):
        Cliente(nome="Murilo", cpf="111.111.111-11")


# Verifica se um cliente recém-criado inicia sem contas vinculadas e com saldo total zerado
def test_cliente_novo_nao_tem_contas(cliente_exemplo):
    assert cliente_exemplo.listar_contas() == []
    assert cliente_exemplo.saldo_total() == 0


# Verifica se adicionar_conta estabelece a associação bidirecional entre cliente e conta
def test_adicionar_conta_liga_os_dois_lados(cliente_exemplo):
    conta = ContaCorrente("1")
    cliente_exemplo.adicionar_conta(conta)
    assert conta in cliente_exemplo.contas
    assert conta.cliente is cliente_exemplo


# Verifica se adicionar a mesma instância de conta mais de uma vez não gera duplicidade
def test_adicionar_a_mesma_conta_duas_vezes_nao_duplica(cliente_exemplo):
    conta = ContaCorrente("1")
    cliente_exemplo.adicionar_conta(conta)
    cliente_exemplo.adicionar_conta(conta)
    assert len(cliente_exemplo.contas) == 1


# Verifica se listar_contas retorna uma cópia protegida da lista interna do cliente
def test_listar_contas_devolve_copia(cliente_exemplo):
    cliente_exemplo.adicionar_conta(ContaCorrente("1"))
    lista = cliente_exemplo.listar_contas()
    lista.clear()
    assert len(cliente_exemplo.contas) == 1


# Verifica se saldo_total soma corretamente os saldos de todas as contas do cliente
def test_saldo_total_soma_todas_as_contas(cliente_exemplo):
    cliente_exemplo.adicionar_conta(ContaCorrente("1", saldo=100.0))
    cliente_exemplo.adicionar_conta(ContaPoupanca("2", saldo=200.0))
    assert cliente_exemplo.saldo_total() == pytest.approx(300.0)


# Verifica se saldo_total contabiliza saldos negativos (uso de limite) na soma geral
def test_saldo_total_considera_saldo_negativo(cliente_exemplo):
    cliente_exemplo.adicionar_conta(ContaCorrente("1", saldo=-50.0))
    cliente_exemplo.adicionar_conta(ContaPoupanca("2", saldo=200.0))
    assert cliente_exemplo.saldo_total() == pytest.approx(150.0)


# Verifica se saldo_total reflete movimentações realizadas diretamente nas contas
def test_saldo_total_acompanha_operacoes(cliente_exemplo):
    conta = ContaCorrente("1", saldo=100.0)
    cliente_exemplo.adicionar_conta(conta)
    conta.depositar(50.0)
    assert cliente_exemplo.saldo_total() == pytest.approx(150.0)


# Verifica se to_dict exporta apenas os atributos cadastrais do cliente (sem a lista de contas)
def test_to_dict_tem_so_os_dados_do_cliente(cliente_exemplo):
    cliente_exemplo.adicionar_conta(ContaCorrente("1"))
    assert cliente_exemplo.to_dict() == {
        "nome": "Alice Barreto Costa",
        "cpf": "52998224725",
        "data_nascimento": "1995-05-15",
        "email": "abc@gmail.com",
        "telefone": "79999123456",
        "endereco": "Rua Secundária, 456. Bairro, Aracaju, Sergipe.",
    }


# Verifica se from_dict reconstrói corretamente um objeto Cliente a partir de um dicionário
def test_from_dict_cria_o_cliente():
    cliente = Cliente.from_dict({"nome": "Bento", "cpf": "111.444.777-35", "email": "b@b.com"})
    assert isinstance(cliente, Cliente)
    assert cliente.nome == "Bento"
    assert cliente.cpf == "11144477735"
    assert cliente.email == "b@b.com"
    assert cliente.data_nascimento == ""
    assert cliente.contas == []


# Verifica se from_dict rejeita dicionários contendo CPF inválido
def test_from_dict_com_cpf_invalido_levanta_erro():
    with pytest.raises(CpfInvalidoError):
        Cliente.from_dict({"nome": "Bento", "cpf": "111.111.111-11"})


# Verifica se converter para dicionário e reconstruir o objeto preserva todos os dados
def test_to_dict_e_from_dict_sao_inversos(cliente_exemplo):
    copia = Cliente.from_dict(cliente_exemplo.to_dict())
    assert copia.to_dict() == cliente_exemplo.to_dict()
