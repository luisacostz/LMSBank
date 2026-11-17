'''
Módulo: agencia.py
Descrição: Classe Agencia. O banco tem apenas UMA agência.
'''

from __future__ import annotations # Permite usar a própria classe como tipo de retorno do método from_dict
from typing import TYPE_CHECKING, List # Permite usar type hinting sem criar import circular

# Será usado apenas para type hinting, não para criar objetos.
if TYPE_CHECKING:
    from conta import Conta

# 
class Agencia:
    # Inicializa a agência com os dados informados. Se não informar, usa valores vazios.
    def __init__(self, numero_agencia: str = "", nome: str = "", telefone: str = "",
                 endereco: str = "", contas: List[Conta] = None) -> None:
        self.numero_agencia = numero_agencia
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    # Adiciona uma conta à agência. Se a conta já estiver na lista, não adiciona de novo.
    def adicionar_conta(self, conta: Conta) -> None:
        if conta not in self.contas:
            self.contas.append(conta)
        conta.agencia = self

    # Remove uma conta da agência. Se a conta não estiver na lista, não faz nada.
    def listar_contas(self) -> List[Conta]:
        return list(self.contas)

    # Retorna o montante total de dinheiro na agência (soma dos saldos das contas).
    def montante_total(self) -> float:
        return sum(conta.saldo for conta in self.contas)

    # 
    def to_dict(self) -> dict:
        # TODO 
        raise NotImplementedError

    #
    @staticmethod
    def from_dict(dados: dict) -> Agencia:
        # TODO 
        raise NotImplementedError
