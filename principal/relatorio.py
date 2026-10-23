"""
Módulo: relatorio.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para gerar relatórios sobre o banco, como calcular o montante total, montante por agência, agência com mais clientes e quantidade de contas conjuntas.
"""
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
    # Calcula o saldo médio das contas com proteção para divisão por zero.
    if not contas:
        return 0.0
    return float(montante_total_banco(contas) / len(contas))


# --- Apelidos (aliases) para garantir compatibilidade com os testes ---
saldo_total_banco = montante_total_banco
contas_saldo_positivo = contas_com_saldo_positivo
maior_saldo = conta_maior_saldo
menor_saldo = conta_menor_saldo


# =====================================================================
# Funções complementares do módulo
# =====================================================================

def montante_por_agencia(contas, numero_agencia):
    total_agencia = 0.0
    for conta in contas:
        if conta["agencia"] == numero_agencia:
            total_agencia += conta["saldo"]
    return total_agencia


def agencia_mais_clientes(contas):
    clientes_por_agencia = {}
    for conta in contas:
        agencia = conta["agencia"]
        if agencia not in clientes_por_agencia:
            clientes_por_agencia[agencia] = []
        for cpf in conta["clientes"]:
            if cpf not in clientes_por_agencia[agencia]:
                clientes_por_agencia[agencia].append(cpf)

    melhor_agencia = False
    maior_quantidade = 0

    for agencia in clientes_por_agencia:
        quantidade = len(clientes_por_agencia[agencia])
        if quantidade > maior_quantidade:
            maior_quantidade = quantidade
            melhor_agencia = agencia
    return melhor_agencia


def contar_contas_conjuntas(contas):
    quantidade = 0
    for conta in contas:
        if len(conta["clientes"]) > 1:
            quantidade += 1
    # Retorna a quantidade de contas conjuntas encontradas
    return quantidade