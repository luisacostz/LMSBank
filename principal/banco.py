'''
Módulo: banco.py
Descrição: Classe Banco. É um SINGLETON: só existe um Banco no programa inteiro, e
todo mundo (console e Flask) o pega com Banco.get_instancia().
Padrão de projeto: SINGLETON.
O banco.json só é lido em iniciar() e só é gravado em encerrar().
'''

from __future__ import annotations
from typing import List
from agencia import Agencia
from cliente import Cliente
from conta import Conta
from dashboard import Dashboard


class Banco:
    _instancia = None  # guarda o único Banco

    def __init__(self) -> None:
        self.agencia: Agencia = None
        self.clientes: List[Cliente] = []
        self.contas: List[Conta] = []

    @staticmethod
    def get_instancia() -> Banco:
        if Banco._instancia is None:
            Banco._instancia = Banco()
        return Banco._instancia

    def iniciar(self, caminho: str = "banco.json") -> None:
        # TODO 
        raise NotImplementedError

    def encerrar(self, caminho: str = "banco.json") -> None:
        # TODO 
        raise NotImplementedError

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        raise NotImplementedError  # TODO 

    def procurar_cliente(self, cpf: str) -> Cliente:
        raise NotImplementedError  # TODO 

    def cadastrar_conta(self, conta: Conta) -> None:
        raise NotImplementedError  # TODO 

    def procurar_conta(self, numero: str) -> Conta:
        raise NotImplementedError  # TODO

    def montar_dashboard(self) -> Dashboard:
        raise NotImplementedError  # TODO 
