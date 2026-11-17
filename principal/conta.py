'''
Módulo: conta.py
Descrição: Classe Abstrata Conta. Guarda o que é comum a todas as contas e define o
fluxo das operações. O que muda de um tipo para outro (saldo disponível e tipo)
fica nas subclasses: ContaCorrente e ContaPoupanca.

Padrão de projeto: TEMPLATE METHOD. O método sacar() define os passos (validar,
conferir saldo, debitar) e chama saldo_disponivel(), que cada subclasse implementa.
'''

from __future__ import annotations # para usar Conta como tipo de retorno de transferir() e from_dict()
import math # para math.isfinite()
from abc import ABC, abstractmethod # para criar classe abstrata
from typing import TYPE_CHECKING # para evitar import circular
from excecoes import OperacaoInvalidaError, SaldoInsuficienteError, ValorInvalidoError # para lançar exceções

# Será usado apenas para type hinting, não para criar objetos. Evita import circular.
if TYPE_CHECKING:
    from agencia import Agencia
    from cliente import Cliente

# Classe abstrata Conta. Define o que é comum a todas as contas e o fluxo das operações.
class Conta(ABC):
    def __init__(self, numero: str, saldo: float = 0.0,
                 cliente: Cliente = None, agencia: Agencia = None) -> None:
        self.numero = numero
        self.saldo = saldo
        self.cliente = cliente
        self.agencia = agencia

    # Métodos que não mudam de uma conta para outra (depositar, sacar, transferir, consultar_saldo)
    # Depositar pede apenas validar o valor e somar ao saldo. O saque precisa conferir o saldo disponível.
    def depositar(self, valor: float) -> None:
        self._validar_valor(valor)
        self.saldo += valor

    # O método sacar() chama saldo_disponivel(), que cada subclasse implementa.
    # Sacar pede validar o valor, conferir o saldo disponível e subtrair do saldo.
    def sacar(self, valor: float) -> None:
        # TEMPLATE METHOD: os passos são sempre estes, o saldo disponível varia.
        self._validar_valor(valor)
        disponivel = self.saldo_disponivel()
        if valor > disponivel:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Disponível: R$ {disponivel:.2f}."
            )
        self.saldo -= valor

    # Transferir pede validar o valor, sacar da conta origem e depositar na conta destino.
    def transferir(self, destino: Conta, valor: float) -> None:
        if destino is None or destino is self:
            raise OperacaoInvalidaError("Escolha uma conta de destino diferente da origem.")
        # Se o saque falhar, a exceção sobe e o destino NÃO recebe nada.
        self.sacar(valor)
        destino.depositar(valor)

    # Consultar saldo apenas devolve o saldo atual (não precisa de validação).
    def consultar_saldo(self) -> float:
        return self.saldo

    # O que muda de uma conta para outra (saldo disponível e tipo) fica nas subclasses: ContaCorrente e ContaPoupanca.
    # Saldo disponível é o que a conta pode gastar agora (a corrente soma o cheque especial).
    @abstractmethod
    def saldo_disponivel(self) -> float:
        '''Quanto a conta pode gastar agora (a corrente soma o cheque especial).'''

    # O tipo da conta é usado no JSON e na exibição para o usuário.
    @abstractmethod
    def tipo(self) -> str:
        '''Nome do tipo: "corrente" ou "poupanca".'''

    # Conversão para o JSON 
    def to_dict(self) -> dict:
        # A conta guarda só o CPF do titular no JSON (não o objeto inteiro).
        return {
            "numero": self.numero,
            "cliente_cpf": self.cliente.cpf if self.cliente else None,
            "saldo": self.saldo,
            "tipo": self.tipo(),
        }

    # Validar valor de depósito, saque ou transferência. Lança ValorInvalidoError se inválido.
    @staticmethod
    def _validar_valor(valor) -> None:
        # O valor deve ser um número positivo (não zero, não negativo, não infinito, não NaN, não booleano).
        if (isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not math.isfinite(valor)
                or valor <= 0):
            raise ValorInvalidoError("O valor deve ser um número positivo.")
