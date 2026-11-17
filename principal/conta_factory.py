'''
Módulo: conta_factory.py
Descrição: Fábrica de contas.
Padrão de projeto: FACTORY METHOD. Quem precisa de uma conta pede para a fábrica 
e informa só o tipo. Só este arquivo conhece as classes concretas, 
então o resto do sistema nunca escreve "if tipo == ...".
'''


from __future__ import annotations # Permite usar a própria classe como tipo de retorno do método from_dict
from typing import TYPE_CHECKING # Permite usar type hinting sem criar import circular
from conta import Conta # Classe abstrata Conta, que define o que é comum a todas as contas e o fluxo das operações.
from conta_corrente import ContaCorrente 
from conta_poupanca import ContaPoupanca
from excecoes import TipoContaInvalidoError # Exceção para tipo de conta inválido.


# Será usado apenas para type hinting, não para criar objetos.
if TYPE_CHECKING:
    from agencia import Agencia
    from cliente import Cliente

# 
class ContaFactory:
    # Para criar um novo tipo de conta põe aqui.
    _TIPOS = {
        "corrente": ContaCorrente,
        "poupanca": ContaPoupanca,
    }

    # Retorna a classe da conta correspondente ao tipo informado.
    @staticmethod
    def _classe_do_tipo(tipo: str):
        # Aceita "Corrente", " poupança ", etc.
        nome = str(tipo).strip().lower().replace("ç", "c").replace("ã", "a")
        classe = ContaFactory._TIPOS.get(nome)
        # Se não encontrou, levanta exceção. Quem chama deve tratar.
        if classe is None:
            raise TipoContaInvalidoError(f'Tipo de conta "{tipo}" inválido. Use "corrente" ou "poupanca".')
        return classe

    # Cria uma conta nova (usada no cadastro). Os limite, taxa vêm do padrão.
    @staticmethod
    def criar(tipo: str, numero: str, cliente: Cliente = None,
              agencia: Agencia = None, saldo: float = 0.0) -> Conta:
        classe = ContaFactory._classe_do_tipo(tipo)
        return classe(numero=numero, saldo=saldo, cliente=cliente, agencia=agencia)

    # Recria uma conta que veio do banco.json. O cliente e a agência já devem ter sido
    # encontrados por quem chama (o Banco procura o cliente pelo "cliente_cpf").
    @staticmethod
    def from_dict(dados: dict, cliente: Cliente = None, agencia: Agencia = None) -> Conta:
        classe = ContaFactory._classe_do_tipo(dados.get("tipo", "corrente"))
        return classe.from_dict(dados, cliente, agencia)
