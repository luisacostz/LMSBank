"""
Módulo: relatorio.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Funções de relatório que trabalham com contas em formato de dicionário: 
montante total, montante por agência, agência com mais clientes,
contas conjuntas, contas com saldo positivo, maior saldo, menor saldo e saldo médio.
Na Etapa 5, o console e o Flask usam as classes (Banco, Agencia, Conta), este módulo
fica como apoio.

Formato esperado de cada conta (dicionário):
    {"numero_conta": "1", "agencia": "0001", "saldo": 100.0, "clientes": ["52998224725"]}
"""

# reduce junta uma lista inteira em um único valor
from functools import reduce


# Montante total do banco usando reduce
def montante_total_banco(contas):
    # Calcula a soma total dos saldos de todas as contas usando reduce.
        # Retorna 0.0 caso a lista esteja vazia
    if not contas:
        return 0.0
    return float(reduce(lambda acumulador, conta: acumulador + conta["saldo"], contas, 0.0))


# Contas com saldo positivo usando filter
def contas_com_saldo_positivo(contas):
    # Filtra e retorna apenas as contas com saldo estritamente maior que zero.
    return list(filter(lambda conta: conta["saldo"] > 0, contas))


# Conta com maior saldo usando max com key
def conta_maior_saldo(contas):
    # Retorna o dicionário completo da conta com o maior saldo.
    # Retorna um dicionário vazio se a lista estiver vazia.
    return max(contas, key=lambda conta: conta["saldo"], default={})


# Conta com menor saldo usando min com key
def conta_menor_saldo(contas):
    # Retorna o dicionário completo da conta com o menor saldo.
    # Retorna um dicionário vazio se a lista estiver vazia.
    return min(contas, key=lambda conta: conta["saldo"], default={})


# Saldo médio das contas
def saldo_medio(contas):
    # Média = total / quantidade de contas. Sem contas, devolve 0.0 para não dividir por zero.
    if not contas:
        return 0.0
    return float(montante_total_banco(contas) / len(contas))


# Texto de cada conta com saldo positivo
def linhas_contas_saldo_positivo(contas):
    # Usa contas_com_saldo_positivo e monta uma frase para cada conta (list comprehension). :.2f mostra o saldo com duas casas decimais.
    return [
        f"Conta: {conta['numero_conta']}, Agência: {conta['agencia']}, Saldo: R$ {conta['saldo']:.2f}"
        for conta in contas_com_saldo_positivo(contas)
    ]


# Montante de uma agência
def montante_por_agencia(contas, numero_agencia):
    # Percorre todas as contas e só soma o saldo das que são da agência pedida.
    total_agencia = 0.0
    for conta in contas:
        if conta["agencia"] == numero_agencia:
            total_agencia += conta["saldo"]
    return total_agencia


# Agência com mais clientes diferentes
def agencia_mais_clientes(contas):
    # Cria um dicionário que mapeia cada agência para uma lista de CPFs únicos de clientes.
    clientes_por_agencia = {}
    for conta in contas:
        agencia = conta["agencia"]
        if agencia not in clientes_por_agencia:
            clientes_por_agencia[agencia] = []
        for cpf in conta["clientes"]:
            if cpf not in clientes_por_agencia[agencia]:
                clientes_por_agencia[agencia].append(cpf)

    # Determina qual agência tem a maior quantidade de clientes diferentes.
    melhor_agencia = False  # continua False se não houver nenhuma conta
    maior_quantidade = 0

    for agencia in clientes_por_agencia:
        quantidade = len(clientes_por_agencia[agencia])
        if quantidade > maior_quantidade:
            maior_quantidade = quantidade
            melhor_agencia = agencia
    return melhor_agencia


# Quantidade de contas conjuntas
def contar_contas_conjuntas(contas):
    # Conta conjunta é a que tem mais de um titular na lista "clientes".
    quantidade = 0
    for conta in contas:
        if len(conta["clientes"]) > 1:
            quantidade += 1
    return quantidade
