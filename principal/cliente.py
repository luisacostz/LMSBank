'''
Módulo: cliente.py
Descrição: Classe Cliente. Um cliente pode ter N contas; cada conta tem 1 cliente.
'''

from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from conta import Conta


class Cliente:
    def __init__(self, nome: str = "", cpf: str = "", data_nascimento: str = "",
                 email: str = "", telefone: str = "", endereco: str = "",
                 contas: List[Conta] = None) -> None:
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    def adicionar_conta(self, conta: Conta) -> None:
        if conta not in self.contas:
            self.contas.append(conta)
        conta.cliente = self  # mantém os dois lados da ligação em sincronia

    def listar_contas(self) -> List[Conta]:
        return list(self.contas)

    def saldo_total(self) -> float:
        return sum(conta.saldo for conta in self.contas)

    def to_dict(self) -> dict:
        # TODO 
        raise NotImplementedError

    @staticmethod
    def from_dict(dados: dict) -> Cliente:
        # TODO 
        raise NotImplementedError
