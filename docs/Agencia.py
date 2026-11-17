from typing import List

class Agencia:
    def __init__(self, numero_agencia: str = "", nome: str = "", telefone: str = "", endereco: str = "", contas: List[Conta] = []) -> None:
        self.numero_agencia = numero_agencia
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.contas = contas

    def adicionar_conta(self, conta: Object) -> None:
        pass

    def listar_contas(self) -> List[Conta]:
        return []

    def montante_total(self) -> float:
        return 0.0

    def to_dict(self) -> dict:
        return None

    @staticmethod
    def from_dict(dados: Object) -> Agencia:
        return None
