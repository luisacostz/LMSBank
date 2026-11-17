'''
Módulo: agencia.py
Descrição: Classe Agencia. O banco tem apenas UMA agência.
'''

# Importa o suporte a anotações de tipo adiadas (evita erro de referência circular)
from __future__ import annotations

# Importa TYPE_CHECKING e List para tipagem estática das listas de objetos
from typing import TYPE_CHECKING, List

# Importa a classe Conta apenas durante a verificação de tipos, evitando importação circular em tempo de execução
if TYPE_CHECKING:
    from conta import Conta


# Classe que representa a agência bancária
class Agencia:
    # Método construtor que inicializa os atributos da agência
    def __init__(self, numero_agencia: str = "", nome: str = "", telefone: str = "",
                 endereco: str = "", contas: List[Conta] = None) -> None:
        self.numero_agencia = numero_agencia
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        # Inicializa a lista de contas da agência (cria lista vazia se nenhuma for passada)
        self.contas = contas if contas is not None else []

    # Método para vincular uma conta à agência
    def adicionar_conta(self, conta: Conta) -> None:
        # Adiciona a conta apenas se ela ainda não estiver registrada na lista
        if conta not in self.contas:
            self.contas.append(conta)
        # Define esta agência como a agência titular da conta
        conta.agencia = self

    # Método para retornar uma cópia da lista de contas cadastradas na agência
    def listar_contas(self) -> List[Conta]:
        return list(self.contas)

    # Método para calcular a soma dos saldos de todas as contas da agência
    def montante_total(self) -> float:
        return sum(conta.saldo for conta in self.contas)

    # Método para converter os dados do objeto Agencia em um dicionário (para salvar em JSON)
    def to_dict(self) -> dict:
        return {
            "numero_agencia": self.numero_agencia,
            "nome": self.nome,
            "telefone": self.telefone,
            "endereco": self.endereco,
        }

    # Método estático para recriar um objeto Agencia a partir de um dicionário (lido do JSON)
    @staticmethod
    def from_dict(dados: dict) -> Agencia:
        return Agencia(
            numero_agencia=dados["numero_agencia"],
            nome=dados.get("nome", ""),
            telefone=dados.get("telefone", ""),
            endereco=dados.get("endereco", ""),
        )
