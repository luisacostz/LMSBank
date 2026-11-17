'''
Teste de unidade para o módulo "dashboard" da pasta "web"
Descrição: Este módulo contém testes de unidade para a função montar_dashboard, que reúne os números exibidos na página do dashboard.
'''

# Importa o pytest e as classes de domínio necessárias para montar o cenário do dashboard
import pytest

from agencia import Agencia
from banco import Banco
from cliente import Cliente
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from dashboard import Dashboard


# Verifica se uma instância padrão de Dashboard inicia com todos os indicadores zerados ou vazios
def test_dashboard_vazio_tem_tudo_zerado():
    dados = Dashboard()
    assert dados.num_clientes == 0
    assert dados.num_contas == 0
    assert dados.saldo_total == 0.0
    assert dados.saldo_medio == 0.0
    assert dados.maior_saldo == 0.0
    assert dados.menor_saldo == 0.0
    assert dados.maior_saldo_conta == ""
    assert dados.menor_saldo_conta == ""


# Verifica se o Dashboard armazena corretamente todos os valores passados na inicialização
def test_dashboard_guarda_os_valores_informados():
    dados = Dashboard(
        num_clientes=2, num_contas=3, saldo_total=5000.0, saldo_medio=5000.0 / 3,
        maior_saldo=5025.0, maior_saldo_conta="2",
        menor_saldo=-45.0, menor_saldo_conta="1", num_agencias=1,
    )
    assert dados.num_clientes == 2
    assert dados.num_agencias == 1
    assert dados.num_contas == 3
    assert dados.saldo_total == 5000.0
    assert dados.maior_saldo_conta == "2"
    assert dados.menor_saldo_conta == "1"


# Verifica a comparação de igualdade e desigualdade gerada pela dataclass Dashboard
def test_dashboards_com_os_mesmos_dados_sao_iguais():
    assert Dashboard(num_clientes=1, saldo_total=10.0) == Dashboard(num_clientes=1, saldo_total=10.0)
    assert Dashboard(num_clientes=1) != Dashboard(num_clientes=2)


# Função auxiliar que cria um banco povoado com agência, clientes e contas para os testes
def montar_banco():
    banco = Banco()
    banco.agencia = Agencia(numero_agencia="0001", nome="Matriz")
    alice = Cliente(nome="Alice", cpf="529.982.247-25")
    bento = Cliente(nome="Bento", cpf="111.444.777-35")
    banco.clientes = [alice, bento]
    banco.contas = [
        ContaCorrente("1", saldo=-45.0, cliente=alice, agencia=banco.agencia),
        ContaCorrente("2", saldo=5025.0, cliente=bento, agencia=banco.agencia),
        ContaPoupanca("3", saldo=20.0, cliente=alice, agencia=banco.agencia),
    ]
    for conta in banco.contas:
        conta.cliente.adicionar_conta(conta)
        banco.agencia.adicionar_conta(conta)
    return banco


# Verifica se montar_dashboard contabiliza corretamente clientes, agência e contas
def test_montar_dashboard_contagens():
    dados = montar_banco().montar_dashboard()
    assert dados.num_clientes == 2
    assert dados.num_agencias == 1
    assert dados.num_contas == 3


# Verifica o cálculo da soma total e da média dos saldos das contas
def test_montar_dashboard_saldo_total_e_medio():
    dados = montar_banco().montar_dashboard()
    assert dados.saldo_total == pytest.approx(5000.0)
    assert dados.saldo_medio == pytest.approx(5000.0 / 3)


# Verifica a identificação do maior saldo e do número da respectiva conta
def test_montar_dashboard_maior_saldo():
    dados = montar_banco().montar_dashboard()
    assert dados.maior_saldo == pytest.approx(5025.0)
    assert dados.maior_saldo_conta == "2"


# Verifica a identificação do menor saldo (incluindo negativo) e da respectiva conta
def test_montar_dashboard_menor_saldo():
    dados = montar_banco().montar_dashboard()
    assert dados.menor_saldo == pytest.approx(-45.0)
    assert dados.menor_saldo_conta == "1"


# Verifica se montar_dashboard retorna indicadores zerados quando o banco não possui registros
def test_montar_dashboard_banco_vazio():
    dados = Banco().montar_dashboard()
    assert dados.num_clientes == 0
    assert dados.num_contas == 0
    assert dados.saldo_total == 0.0
    assert dados.saldo_medio == 0.0
    assert dados.maior_saldo == 0.0
    assert dados.menor_saldo == 0.0
    assert dados.maior_saldo_conta == ""
    assert dados.menor_saldo_conta == ""
