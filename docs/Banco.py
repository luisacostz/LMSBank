from typing import List

class Banco:
    def __init__(self, _instancia: Banco = None, agencia: Agencia = None, clientes: List[Cliente] = [], contas: List[Conta] = []) -> None:
        self._instancia = _instancia
        self.agencia = agencia
        self.clientes = clientes
        self.contas = contas

    @staticmethod
    def get_instancia() -> Banco:
        return None

    def iniciar(self) -> None:
        pass

    def encerrar(self) -> None:
        pass

    def cadastrar_cliente(self, cliente: Object) -> None:
        pass

    def procurar_cliente(self, cpf: Object) -> Cliente:
        return None

    def cadastrar_conta(self, conta: Object) -> None:
        pass

    def procurar_conta(self, numero: Object) -> Conta:
        return None

    def montar_dashboard(self) -> Dashboard:
        return None
