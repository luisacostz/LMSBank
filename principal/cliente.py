'''
Módulo: cliente.py
Descrição: Classe Cliente. Um cliente pode ter N contas; cada conta tem 1 cliente.
'''

# Importa o suporte a anotações de tipo adiadas (evita erro de referência circular)
from __future__ import annotations

# Importa TYPE_CHECKING e List para tipagem estática das listas de objetos
from typing import TYPE_CHECKING, List

# Importa as funções utilitárias para formatar e validar o número de CPF
from cpf import limpar_cpf, validar_cpf

# Importa a exceção personalizada lançada quando o CPF informado é inválido
from excecoes import CpfInvalidoError

# Importa a classe Conta apenas durante a verificação de tipos, evitando importação circular em tempo de execução
if TYPE_CHECKING:
    from conta import Conta


# Classe que representa um cliente do banco
class Cliente:
    # Método construtor que valida o CPF e inicializa os atributos do cliente
    def __init__(self, nome: str, cpf: str, data_nascimento: str = "",
                 email: str = "", telefone: str = "", endereco: str = "",
                 contas: List[Conta] = None) -> None:
        # Remove caracteres não numéricos do CPF informado
        cpf_limpo = limpar_cpf(str(cpf))
        # Verifica se o CPF é válido; caso contrário, lança uma exceção
        if not validar_cpf(cpf_limpo):
            raise CpfInvalidoError(
                "CPF inválido! Precisa ter 11 números e os 2 últimos dígitos (verificadores) corretos."
            )
        self.nome = nome
        self.cpf = cpf_limpo
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        # Inicializa a lista de contas do cliente (cria lista vazia se nenhuma for passada)
        self.contas = contas if contas is not None else []

    # Método para vincular uma conta ao cliente (1 cliente pode ter N contas)
    def adicionar_conta(self, conta: Conta) -> None:
        # Adiciona a conta apenas se ela ainda não estiver na lista do cliente
        if conta not in self.contas:
            self.contas.append(conta)
        # Define este cliente como o titular da conta
        conta.cliente = self

    # Método para retornar uma cópia da lista de contas pertencentes ao cliente
    def listar_contas(self) -> List[Conta]:
        return list(self.contas)

    # Método para calcular a soma dos saldos de todas as contas do cliente
    def saldo_total(self) -> float:
        return sum(conta.saldo for conta in self.contas)

    # Método para converter os dados do objeto Cliente em um dicionário (para salvar em JSON)
    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
        }

    # Método estático para recriar um objeto Cliente a partir de um dicionário (lido do JSON)
    @staticmethod
    def from_dict(dados: dict) -> Cliente:
        return Cliente(
            nome=dados["nome"],
            cpf=dados["cpf"],
            data_nascimento=dados.get("data_nascimento", ""),
            email=dados.get("email", ""),
            telefone=dados.get("telefone", ""),
            endereco=dados.get("endereco", ""),
        )
