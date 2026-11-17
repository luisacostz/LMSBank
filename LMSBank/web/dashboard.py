"""
Módulo: dashboard.py
Responsáveis: Murilo Santana e Sarah Beatriz

As funções de saldo (reduce, filter, max e min) foram feitas em principal/relatorio.py e são importadas aqui, para não repetir código.
"""

# O app.py já coloca a pasta "principal" no caminho do Python antes de importar este arquivo
from relatorio import (
    contas_saldo_positivo,  # Contas com saldo maior que zero (filter)
    saldo_total_banco,      # Soma de todos os saldos (reduce)
    maior_saldo,            # Conta com o maior saldo (max com key)
    menor_saldo,            # Conta com o menor saldo (min com key)
    saldo_medio,            # Média dos saldos
)

# Função que monta o dicionário com os dados do dashboard
def montar_dashboard(clientes, agencias, contas):
    # Maior e menor saldo devolvem o dicionário completo da conta, então precisamos extrair o saldo e o número da conta.
    conta_maior = maior_saldo(contas)
    conta_menor = menor_saldo(contas)
    # Monta o dicionário com os dados do dashboard, incluindo número de clientes, agências, contas, saldo total, saldo médio, maior e menor saldo e os números das contas correspondentes.
    return {
        "num_clientes": len(clientes),
        "num_agencias": len(agencias),
        "num_contas": len(contas),
        "saldo_total": saldo_total_banco(contas),
        "saldo_medio": saldo_medio(contas),
        "maior_saldo": conta_maior.get("saldo", 0.0),
        "maior_saldo_conta": conta_maior.get("numero", ""),
        "menor_saldo": conta_menor.get("saldo", 0.0),
        "menor_saldo_conta": conta_menor.get("numero", ""),
    }