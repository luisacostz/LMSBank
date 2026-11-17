'''
Módulo: dashboard.py
Descrição: Classe só com os números do painel.
'''

# Importa dataclass para simplificar a criação da classe de dados
from dataclasses import dataclass


# Classe que armazena as métricas financeiras do painel geral
@dataclass
class Dashboard:
    num_clientes: int = 0
    num_contas: int = 0
    saldo_total: float = 0.0
    saldo_medio: float = 0.0
    maior_saldo: float = 0.0
    maior_saldo_conta: str = ""
    menor_saldo: float = 0.0
    menor_saldo_conta: str = ""
    num_agencias: int = 1
