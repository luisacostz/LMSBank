'''
Módulo: conta_corrente.py
Descrição: Conta corrente. Tem cheque especial: pode ficar negativa até o limite.
'''

from __future__ import annotations # Permite usar a própria classe como tipo de retorno do método from_dict
from typing import TYPE_CHECKING # Permite usar type hinting sem criar import circular
from conta import Conta # Classe abstrata Conta, que define o que é comum a todas as contas e o fluxo das operações.

# Será usado apenas para type hinting, não para criar objetos.
if TYPE_CHECKING:
    from agencia import Agencia
    from cliente import Cliente

LIMITE_PADRAO = 500.0

# Classe ContaCorrente.
class ContaCorrente(Conta):
    def __init__(self, numero: str, saldo: float = 0.0, cliente: Cliente = None,
                 agencia: Agencia = None, limite: float = LIMITE_PADRAO) -> None:
        super().__init__(numero, saldo, cliente, agencia)
        self.limite = limite

    # Saldo disponível é o que a conta pode gastar agora (a corrente soma o cheque especial).
    def saldo_disponivel(self) -> float:
        # Saldo + cheque especial. Ex.: saldo 100 e limite 500 = pode gastar 600.
        return self.saldo + self.limite

    # O tipo da conta é usado no JSON e na exibição para o usuário.
    def tipo(self) -> str:
        return "corrente"

    # Conversão para o JSON. Adiciona o limite ao dicionário.
    def to_dict(self) -> dict:
        dados = super().to_dict()   # numero, cliente_cpf, saldo, tipo
        dados["limite"] = self.limite
        return dados

    # Cria uma conta corrente a partir de um dicionário. O cliente e a agência podem ser passados como argumentos.
    @classmethod
    def from_dict(cls, dados: dict, cliente: Cliente = None,
                  agencia: Agencia = None) -> ContaCorrente:
        return cls(
            numero=dados["numero"],
            saldo=dados.get("saldo", 0.0),
            cliente=cliente,
            agencia=agencia,
            limite=dados.get("limite", LIMITE_PADRAO),
        )
