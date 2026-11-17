from typing import List

class Cliente:
    def __init__(self, nome: str = "", cpf: str = "", data_nascimento: str = "", email: str = "", telefone: str = "", endereco: str = "", contas: List[Conta] = []) -> None:
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.contas = contas

    def adicionar_conta(self, conta: Object) -> None:
        pass

    def listar_contas(self) -> List[Conta]:
        return []

    def saldo_total(self) -> float:
        return 0.0

    def to_dict(self) -> dict:
        return None

    @staticmethod
    def from_dict(dados: Object) -> Cliente:
        return None
