# Permite usar anotações de tipo que referenciam a própria classe Banco.
from __future__ import annotations
# Fornece List para indicar os tipos das coleções de clientes e contas.
from typing import List

# Importa a entidade que representa a agência do banco.
from agencia import Agencia
# Importa as funções e o caminho padrão usados para ler e gravar os dados JSON.
from armazenamento import CAMINHO_PADRAO, gravar_json, ler_json
# Importa a entidade que representa cada cliente.
from cliente import Cliente
# Importa a classe base das contas bancárias.
from conta import Conta
# Importa a fábrica que reconstrói contas conforme o tipo salvo.
from conta_factory import ContaFactory
# Importa a função que normaliza a representação do CPF.
from cpf import limpar_cpf
# Importa a estrutura usada para apresentar os indicadores do banco.
from dashboard import Dashboard
# Importa a exceção usada para sinalizar operações incompatíveis com os dados.
from excecoes import OperacaoInvalidaError


# Centraliza os dados e as operações de cadastro, consulta e persistência do banco.
class Banco:
    _instancia = None

    def __init__(self) -> None:
        # Inicializa as referências da agência e as listas mantidas pelo banco.
        self.agencia: Agencia = None
        self.clientes: List[Cliente] = []
        self.contas: List[Conta] = []

    @staticmethod
    def get_instancia() -> Banco:
        # Retorna a instância única do banco, criando-a na primeira chamada.
        if Banco._instancia is None:
            Banco._instancia = Banco()
        return Banco._instancia

    def iniciar(self, caminho: str = CAMINHO_PADRAO) -> None:
        # Carrega os dados do arquivo e reconstrói as relações entre agência, clientes e contas.
        dados = ler_json(caminho)

        self.agencia = None
        self.clientes = []
        self.contas = []

        if dados.get("agencia"):
            self.agencia = Agencia.from_dict(dados["agencia"])

        for dados_cliente in dados.get("clientes", []):
            self.clientes.append(Cliente.from_dict(dados_cliente))

        for dados_conta in dados.get("contas", []):
            cpf = dados_conta.get("cliente_cpf")
            cliente = self.procurar_cliente(cpf) if cpf else None
            if cpf and cliente is None:
                raise OperacaoInvalidaError(
                    f"A conta {dados_conta.get('numero')} pertence a um CPF não cadastrado: {cpf}."
                )
            conta = ContaFactory.from_dict(dados_conta, cliente=cliente, agencia=self.agencia)
            if cliente is not None:
                cliente.adicionar_conta(conta)
            if self.agencia is not None:
                self.agencia.adicionar_conta(conta)
            self.contas.append(conta)

        for conta in self.contas:
            if conta.tipo() == "poupanca":
                conta.aplicar_rendimento()

    def encerrar(self, caminho: str = CAMINHO_PADRAO) -> None:
        # Converte os objetos atuais para dicionários e grava o estado do banco em JSON.
        dados = {
            "agencia": self.agencia.to_dict() if self.agencia else None,
            "clientes": [cliente.to_dict() for cliente in self.clientes],
            "contas": [conta.to_dict() for conta in self.contas],
        }
        gravar_json(dados, caminho)

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        # Impede CPFs duplicados e adiciona o cliente à coleção do banco.
        if self.procurar_cliente(cliente.cpf) is not None:
            raise OperacaoInvalidaError("Este CPF já está cadastrado no sistema!")
        self.clientes.append(cliente)

    def procurar_cliente(self, cpf: str) -> Cliente:
        # Normaliza o CPF e devolve o cliente correspondente, se estiver cadastrado.
        cpf_limpo = limpar_cpf(str(cpf))
        for cliente in self.clientes:
            if cliente.cpf == cpf_limpo:
                return cliente
        return None

    def cadastrar_conta(self, conta: Conta) -> None:
        # Valida a unicidade do número e associa a conta ao cliente, agência e banco.
        if self.procurar_conta(conta.numero) is not None:
            raise OperacaoInvalidaError("Este número de conta já está no sistema!")
        if conta.agencia is None:
            conta.agencia = self.agencia
        if conta.cliente is not None:
            conta.cliente.adicionar_conta(conta)
        if conta.agencia is not None:
            conta.agencia.adicionar_conta(conta)
        self.contas.append(conta)

    def procurar_conta(self, numero: str) -> Conta:
        # Localiza uma conta pelo número normalizado ou devolve None se não existir.
        numero_limpo = str(numero).strip()
        for conta in self.contas:
            if conta.numero == numero_limpo:
                return conta
        return None

    def montar_dashboard(self) -> Dashboard:
        # Calcula as contagens e os indicadores de saldo para o painel do banco.
        dashboard = Dashboard(
            num_clientes=len(self.clientes),
            num_contas=len(self.contas),
            num_agencias=1 if self.agencia is not None else 0,
        )
        if not self.contas:
            return dashboard
        maior = max(self.contas, key=lambda conta: conta.saldo)
        menor = min(self.contas, key=lambda conta: conta.saldo)
        dashboard.saldo_total = sum(conta.saldo for conta in self.contas)
        dashboard.saldo_medio = dashboard.saldo_total / len(self.contas)
        dashboard.maior_saldo = maior.saldo
        dashboard.maior_saldo_conta = maior.numero
        dashboard.menor_saldo = menor.saldo
        dashboard.menor_saldo_conta = menor.numero
        return dashboard
