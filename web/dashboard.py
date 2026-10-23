"""
Módulo: dashboard.py
Responsáveis: Murilo Santana e Sarah Beatriz

Lógica Python pura do dashboard (sem HTML, sem Flask).
As funções de saldo (reduce, filter, max e min) foram feitas pela Sarah em
principal/relatorio.py e são importadas aqui, para não repetir código.

Os dados chegam como no resto do projeto: listas de dicionários.
  conta   = {"numero", "clientes", "agencia", "saldo", "tipo", ...}
  cliente = {"nome", "cpf", ...}
  agencia = {"numero_agencia", "nome", ...}
"""

# O app.py já coloca a pasta "principal" no caminho do Python antes de importar este arquivo
from relatorio import (
    contas_saldo_positivo,  # Contas com saldo maior que zero (filter)
    saldo_total_banco,      # Soma de todos os saldos (reduce)
    maior_saldo,            # Conta com o maior saldo (max com key)
    menor_saldo,            # Conta com o menor saldo (min com key)
    saldo_medio,            # Média dos saldos
)


def montar_dashboard(clientes, agencias, contas):
    """Junta tudo num dicionário que o template dashboard.html consome.

    Chaves esperadas pelo template (não renomear sem avisar quem faz o HTML):
        num_clientes       int
        num_agencias       int
        num_contas         int
        saldo_total        float | None
        saldo_medio        float | None
        maior_saldo        float | None   (valor do maior saldo)
        maior_saldo_conta  str   | None   (número da conta dona do maior saldo)
        menor_saldo        float | None
        menor_saldo_conta  str   | None

    Use None nos campos que não puder calcular (ex.: banco sem contas), pois
    o template mostra "—"/"a fazer" sem quebrar.
    """
    # Maior e menor saldo devolvem a conta inteira (dicionário) ou None sem contas.
    conta_maior = maior_saldo(contas)
    conta_menor = menor_saldo(contas)
    return {
        "num_clientes": len(clientes),
        "num_agencias": len(agencias),
        "num_contas": len(contas),
        "saldo_total": saldo_total_banco(contas) if contas else None,
        "saldo_medio": saldo_medio(contas) if contas else None,
        "maior_saldo": conta_maior["saldo"] if conta_maior else None,
        "maior_saldo_conta": conta_maior["numero"] if conta_maior else None,
        "menor_saldo": conta_menor["saldo"] if conta_menor else None,
        "menor_saldo_conta": conta_menor["numero"] if conta_menor else None,
    }
