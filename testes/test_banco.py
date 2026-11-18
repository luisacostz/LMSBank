# Lê e escreve o arquivo JSON usado nos cenários de persistência.
import json
# Fornece datas para preparar e conferir os rendimentos das contas poupança.
from datetime import date

# Disponibiliza fixtures e verificações auxiliares do pytest.
import pytest

# Importa a classe principal que está sendo testada.
from banco import Banco
# Importa a entidade usada nos testes de cadastro de clientes.
from cliente import Cliente
# Importa o tipo concreto esperado para contas correntes.
from conta_corrente import ContaCorrente
# Importa a fábrica usada para criar contas nos testes.
from conta_factory import ContaFactory
# Importa o tipo concreto esperado para contas poupança.
from conta_poupanca import ContaPoupanca
# Importa a exceção esperada em operações inválidas.
from excecoes import OperacaoInvalidaError

DADOS = {
    "agencia": {"numero_agencia": "0001", "nome": "Sede", "telefone": "1111-2222", "endereco": "Rua A"},
    "clientes": [
        {"nome": "Alice", "cpf": "52998224725", "data_nascimento": "1995-05-15",
         "email": "a@a.com", "telefone": "1", "endereco": "Rua B"}
    ],
    "contas": [
        {"numero": "1", "cliente_cpf": "52998224725", "saldo": 100.0, "tipo": "corrente", "limite": 500.0},
        {"numero": "2", "cliente_cpf": "52998224725", "saldo": 200.0, "tipo": "poupanca",
         "taxa_rendimento": 0.005, "ultimo_rendimento": date.today().isoformat()},
    ],
}


@pytest.fixture
def caminho(tmp_path):
    # Prepara um arquivo temporário de banco e o fornece ao teste que solicitou a fixture.
    arquivo = tmp_path / "banco.json"
    arquivo.write_text(json.dumps(DADOS), encoding="utf-8")
    return str(arquivo)


def test_get_instancia_devolve_sempre_o_mesmo_objeto():
    # Confirma que o acesso repetido ao singleton devolve o mesmo objeto.
    assert Banco.get_instancia() is Banco.get_instancia()


def test_iniciar_cria_objetos_e_liga_tudo(caminho):
    # Verifica a reconstrução dos objetos e de suas ligações a partir do JSON.
    banco = Banco()
    banco.iniciar(caminho)
    assert banco.agencia.numero_agencia == "0001"
    assert len(banco.clientes) == 1
    assert len(banco.contas) == 2
    alice = banco.procurar_cliente("529.982.247-25")
    assert alice is banco.contas[0].cliente
    assert len(alice.contas) == 2
    assert len(banco.agencia.contas) == 2
    assert isinstance(banco.contas[0], ContaCorrente)
    assert isinstance(banco.contas[1], ContaPoupanca)


def test_iniciar_aplica_rendimento_da_poupanca(tmp_path):
    # Confirma que iniciar aplica os rendimentos vencidos somente à poupança.
    dados = json.loads(json.dumps(DADOS))
    dados["contas"][1]["ultimo_rendimento"] = "2000-01-01"
    arquivo = tmp_path / "banco.json"
    arquivo.write_text(json.dumps(dados), encoding="utf-8")
    banco = Banco()
    banco.iniciar(str(arquivo))
    assert banco.procurar_conta("2").saldo > 200.0
    assert banco.procurar_conta("2").ultimo_rendimento > date(2000, 1, 1)
    assert banco.procurar_conta("1").saldo == 100.0


def test_iniciar_sem_arquivo_comeca_vazio(tmp_path):
    # Confirma que um arquivo ausente resulta em um banco sem dados cadastrados.
    banco = Banco()
    banco.iniciar(str(tmp_path / "nao_existe.json"))
    assert banco.agencia is None
    assert banco.clientes == []
    assert banco.contas == []


def test_iniciar_com_conta_de_cpf_desconhecido_falha(tmp_path):
    # Verifica que uma conta sem cliente correspondente gera erro de operação.
    dados = json.loads(json.dumps(DADOS))
    dados["contas"][0]["cliente_cpf"] = "11144477735"
    arquivo = tmp_path / "banco.json"
    arquivo.write_text(json.dumps(dados), encoding="utf-8")
    with pytest.raises(OperacaoInvalidaError):
        Banco().iniciar(str(arquivo))


def test_encerrar_grava_e_iniciar_le_de_volta(caminho, tmp_path):
    # Confirma que o estado gravado pode ser carregado novamente sem perder dados.
    banco = Banco()
    banco.iniciar(caminho)
    banco.procurar_conta("1").depositar(50.0)
    saida = str(tmp_path / "saida.json")
    banco.encerrar(saida)
    outro = Banco()
    outro.iniciar(saida)
    assert outro.procurar_conta("1").saldo == pytest.approx(150.0)
    assert outro.procurar_conta("2").tipo() == "poupanca"
    assert outro.agencia.nome == "Sede"


def test_encerrar_so_grava_no_json(caminho):
    # Confirma que as alterações em memória só chegam ao arquivo ao encerrar.
    banco = Banco()
    banco.iniciar(caminho)
    banco.procurar_conta("1").depositar(50.0)
    assert json.load(open(caminho, encoding="utf-8"))["contas"][0]["saldo"] == 100.0


def test_cadastrar_cliente_e_procurar(cliente_exemplo):
    # Verifica o cadastro de cliente e a busca por CPF formatado ou inexistente.
    banco = Banco()
    banco.cadastrar_cliente(cliente_exemplo)
    assert banco.procurar_cliente("529.982.247-25") is cliente_exemplo
    assert banco.procurar_cliente("00000000000") is None


def test_cadastrar_cliente_duplicado_falha(cliente_exemplo):
    # Confirma que o banco rejeita um cliente com CPF já cadastrado.
    banco = Banco()
    banco.cadastrar_cliente(cliente_exemplo)
    with pytest.raises(OperacaoInvalidaError):
        banco.cadastrar_cliente(Cliente(nome="Outra", cpf="52998224725"))


def test_cadastrar_conta_liga_cliente_e_agencia(cliente_exemplo, agencia_exemplo):
    # Verifica o cadastro da conta e seus vínculos com o cliente e a agência.
    banco = Banco()
    banco.agencia = agencia_exemplo
    banco.cadastrar_cliente(cliente_exemplo)
    conta = ContaFactory.criar("corrente", "10", cliente=cliente_exemplo, agencia=agencia_exemplo)
    banco.cadastrar_conta(conta)
    assert banco.procurar_conta("10") is conta
    assert conta in cliente_exemplo.contas
    assert conta in agencia_exemplo.contas


def test_cadastrar_conta_duplicada_falha(cliente_exemplo, agencia_exemplo):
    # Confirma que o banco rejeita números de conta já utilizados.
    banco = Banco()
    banco.agencia = agencia_exemplo
    banco.cadastrar_conta(ContaFactory.criar("corrente", "10", cliente=cliente_exemplo))
    with pytest.raises(OperacaoInvalidaError):
        banco.cadastrar_conta(ContaFactory.criar("poupanca", "10", cliente=cliente_exemplo))


def test_procurar_conta_inexistente_devolve_none():
    # Confirma que a busca por número desconhecido não encontra uma conta.
    assert Banco().procurar_conta("999") is None
