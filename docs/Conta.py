from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self, numero: str = "", saldo: float = 0.0, cliente: Cliente = None, agencia: Agencia = None) -> None:
        self.numero = numero
        self.saldo = saldo
        self.cliente = cliente
        self.agencia = agencia

    def depositar(self, valor: Object) -> None:
        pass

    def sacar(self, valor: Object) -> None:
        pass

    def transferir(self, destino: Object, valor: Object) -> None:
        pass

    def consultar_saldo(self) -> float:
        return 0.0

    @abstractmethod
    def saldo_disponivel(self) -> float:
        pass

    @abstractmethod
    def tipo(self) -> str:
        pass

    def to_dict(self) -> dict:
        return None
