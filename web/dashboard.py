"""
Módulo: dashboard.py
Responsáveis: Murilo Santana e Sarah Beatriz

Lógica Python pura do dashboard (sem HTML, sem Flask).

ESTADO: esqueleto. Cada função abaixo devolve None até ser implementada.
O app (app.py + templates) já está pronto para consumir estas funções:
enquanto uma delas devolver None, a tela mostra "a fazer" no lugar do
valor, então o site continua funcionando normalmente durante o
desenvolvimento. É só trocar o `return None` pela implementação.

Os dados chegam como no resto do projeto: listas de dicionários.
  conta   = {"numero", "clientes", "agencia", "saldo", "tipo", ...}
  cliente = {"nome", "cpf", ...}
  agencia = {"numero_agencia", "nome", ...}
"""


def contas_saldo_positivo(contas):
    """Devolve a lista só com as contas de saldo > 0.

    Dica: list comprehension ou filter().
    Usada na página /contas?saldo=positivo.
    Obs.: lista vazia [] é um resultado válido ("nenhuma conta positiva");
    só devolva None enquanto a função não estiver implementada.
    """
    # TODO (Murilo/Sarah)
    return None


def saldo_total_banco(contas):
    """Devolve a soma dos saldos de todas as contas (float).

    Dica: sum() + generator/comprehension.
    """
    # TODO (Murilo/Sarah)
    return None


def maior_saldo(contas):
    """Devolve a CONTA (dict) com o maior saldo, ou None se não há contas.

    Dica: max(contas, key=lambda conta: conta["saldo"]).
    """
    # TODO (Murilo/Sarah)
    return None


def menor_saldo(contas):
    """Devolve a CONTA (dict) com o menor saldo, ou None se não há contas.

    Dica: min(contas, key=lambda conta: conta["saldo"]).
    """
    # TODO (Murilo/Sarah)
    return None


def saldo_medio(contas):
    """Devolve o saldo médio por conta (float).

    Cuidado: com lista vazia, não divida por zero (devolva 0.0).
    """
    # TODO (Murilo/Sarah)
    return None


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
    # Os três contadores são triviais e já ficam prontos.
    # Os demais: trocar None pelas chamadas às funções acima.
    return {
        "num_clientes": len(clientes),
        "num_agencias": len(agencias),
        "num_contas": len(contas),
        "saldo_total": None,
        "saldo_medio": None,
        "maior_saldo": None,
        "maior_saldo_conta": None,
        "menor_saldo": None,
        "menor_saldo_conta": None,
    }
