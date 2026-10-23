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
    # Compreensão de listas: pega o saldo só das contas da agência escolhida e soma
    saldos_da_agencia = [conta["saldo"] for conta in contas if conta["agencia"] == numero_agencia]
    return float(sum(saldos_da_agencia))


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
    # Compreensão de listas: guarda só as contas com mais de um titular
    conjuntas = [conta for conta in contas if len(conta["clientes"]) > 1]
    # Retorna a quantidade de contas conjuntas encontradas
    return len(conjuntas)


# =====================================================================
# Funções com compreensão de listas (etapa 4)
# =====================================================================

# Lista só os saldos das contas
def lista_de_saldos(contas):
    return [conta["saldo"] for conta in contas]


# Lista os números das contas com saldo positivo
def numeros_contas_saldo_positivo(contas):
    # Reaproveita o filter de contas_com_saldo_positivo e extrai só o número de cada conta
    return [conta["numero"] for conta in contas_com_saldo_positivo(contas)]


# Lista os nomes dos clientes que são titulares de contas com saldo positivo
def clientes_com_saldo_positivo(clientes, contas):
    # Conjunto (set) com os CPFs dos titulares de contas positivas
    cpfs_positivos = {cpf for conta in contas_com_saldo_positivo(contas) for cpf in conta["clientes"]}
    return [cliente["nome"] for cliente in clientes if cliente["cpf"] in cpfs_positivos]


# Monta o texto das contas com saldo positivo para exibir no console
def linhas_contas_saldo_positivo(contas):
    return [
        f"Conta {conta['numero']} | Agência {conta['agencia']} | {conta['tipo']} | R$ {conta['saldo']:.2f}"
        for conta in contas_com_saldo_positivo(contas)
    ]
