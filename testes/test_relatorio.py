'''
Teste de unidade para o módulo "relatorio" do pacote "principal"
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém testes de unidade para as funções do módulo "relatorio.py", incluindo cálculo do montante total, montante por agência, agência com mais clientes, quantidade de contas conjuntas, contas com saldo positivo, maior saldo, menor saldo e saldo médio.
'''

# Importa o pytest e as classes de domínio utilizadas nos testes da agência
import pytest

from agencia import Agencia
from cliente import Cliente
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca


# Verifica se uma agência recém-criada inicia sem contas vinculadas e com montante zerado
def test_agencia_nova_esta_vazia(agencia_exemplo):
    assert agencia_exemplo.listar_contas() == []
    assert agencia_exemplo.montante_total() == 0


# Verifica se adicionar_conta estabelece a associação bidirecional entre agência e conta
def test_adicionar_conta_liga_os_dois_lados(agencia_exemplo):
    conta = ContaCorrente("1")
    agencia_exemplo.adicionar_conta(conta)
    assert conta in agencia_exemplo.contas
    assert conta.agencia is agencia_exemplo


# Verifica se adicionar a mesma conta mais de uma vez não gera duplicidade na agência
def test_adicionar_a_mesma_conta_duas_vezes_nao_duplica(agencia_exemplo):
    conta = ContaCorrente("1")
    agencia_exemplo.adicionar_conta(conta)
    agencia_exemplo.adicionar_conta(conta)
    assert len(agencia_exemplo.contas) == 1


# Verifica se listar_contas retorna uma cópia protegida da lista interna da agência
def test_listar_contas_devolve_copia(agencia_exemplo):
    agencia_exemplo.adicionar_conta(ContaCorrente("1"))
    lista = agencia_exemplo.listar_contas()
    lista.clear()
    assert len(agencia_exemplo.contas) == 1


# Verifica se montante_total soma corretamente os saldos de todas as contas da agência
def test_montante_total_soma_os_saldos(agencia_exemplo):
    agencia_exemplo.adicionar_conta(ContaCorrente("1", saldo=100.0))
    agencia_exemplo.adicionar_conta(ContaPoupanca("2", saldo=50.0))
    agencia_exemplo.adicionar_conta(ContaCorrente("3", saldo=25.0))
    assert agencia_exemplo.montante_total() == pytest.approx(175.0)


# Verifica se montante_total contabiliza saldos negativos (uso de limite) no cálculo geral
def test_montante_total_com_saldo_negativo(agencia_exemplo):
    agencia_exemplo.adicionar_conta(ContaCorrente("1", saldo=-45.0))
    agencia_exemplo.adicionar_conta(ContaCorrente("2", saldo=5025.0))
    agencia_exemplo.adicionar_conta(ContaPoupanca("3", saldo=20.0))
    assert agencia_exemplo.montante_total() == pytest.approx(5000.0)


# Verifica se montante_total acompanha transferências e depósitos realizados nas contas
def test_montante_total_acompanha_operacoes(agencia_exemplo):
    origem = ContaCorrente("1", saldo=100.0)
    destino = ContaPoupanca("2", saldo=10.0)
    agencia_exemplo.adicionar_conta(origem)
    agencia_exemplo.adicionar_conta(destino)
    origem.transferir(destino, 60.0)
    assert agencia_exemplo.montante_total() == pytest.approx(110.0)
    origem.depositar(40.0)
    assert agencia_exemplo.montante_total() == pytest.approx(150.0)


# Verifica se o montante total da agência equivale à soma dos saldos totais de seus clientes
def test_montante_da_agencia_bate_com_a_soma_dos_clientes(agencia_exemplo):
    alice = Cliente(nome="Alice", cpf="529.982.247-25")
    bento = Cliente(nome="Bento", cpf="111.444.777-35")
    contas = [
        (alice, ContaCorrente("1", saldo=100.0)),
        (alice, ContaPoupanca("2", saldo=200.0)),
        (bento, ContaCorrente("3", saldo=-30.0)),
    ]
    for cliente, conta in contas:
        cliente.adicionar_conta(conta)
        agencia_exemplo.adicionar_conta(conta)
    assert agencia_exemplo.montante_total() == pytest.approx(alice.saldo_total() + bento.saldo_total())


# Verifica se to_dict exporta apenas os dados cadastrais da agência (sem a lista de contas)
def test_to_dict_tem_so_os_dados_da_agencia(agencia_exemplo):
    agencia_exemplo.adicionar_conta(ContaCorrente("1"))
    assert agencia_exemplo.to_dict() == {
        "numero_agencia": "0001",
        "nome": "Sede",
        "telefone": "1111-2222",
        "endereco": "Rua Principal, 123. Centro, Aracaju, Sergipe.",
    }


# Verifica se from_dict reconstrói corretamente um objeto Agencia a partir de um dicionário
def test_from_dict_cria_a_agencia():
    agencia = Agencia.from_dict({"numero_agencia": "0002", "nome": "Filial"})
    assert isinstance(agencia, Agencia)
    assert agencia.numero_agencia == "0002"
    assert agencia.nome == "Filial"
    assert agencia.telefone == ""
    assert agencia.endereco == ""
    assert agencia.contas == []


# Verifica se converter para dicionário e reconstruir o objeto preserva os dados da agência
def test_to_dict_e_from_dict_sao_inversos(agencia_exemplo):
    copia = Agencia.from_dict(agencia_exemplo.to_dict())
    assert copia.to_dict() == agencia_exemplo.to_dict()
