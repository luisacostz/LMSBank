"""
Módulo: relatorio.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para gerar relatórios sobre o banco, como calcular o montante total, montante por agência, agência com mais clientes e quantidade de contas conjuntas.
"""

# Função para calcular o montante total do banco
def montante_total_banco(contas):
    # Inicializa a variável total com 0.0 para acumular o saldo de todas as contas
    total = 0.0
    # Percorre a lista de contas e soma o saldo de cada conta ao total
    for conta in contas:
        total += conta["saldo"]
    return total


# Função para calcular o montante total de uma agência específica
def montante_por_agencia(contas, numero_agencia):
    # Inicializa a variável total_agencia com 0.0 para acumular o saldo das contas da agência
    total_agencia = 0.0
    # Percorre a lista de contas e, se a conta pertencer à agência especificada, soma o saldo ao total_agencia
    for conta in contas:
        if conta["agencia"] == numero_agencia:
            total_agencia += conta["saldo"]
    return total_agencia


# Função para encontrar a agência com mais clientes 
def agencia_mais_clientes(contas):
    # Cria um dicionário para armazenar os clientes por agência
    clientes_por_agencia = {}
    # Percorre a lista de contas para contar os clientes únicos por agência
    for conta in contas:
        # Acesso em O(1) pelo nome da chave correspondente
        agencia = conta["agencia"]
        # Se a agência ainda não estiver no dicionário, inicializa uma lista vazia para ela
        if agencia not in clientes_por_agencia:
            clientes_por_agencia[agencia] = []
        # Adiciona os CPFs dos clientes da conta à lista da agência, evitando duplicatas
        for cpf in conta["clientes"]:
            if cpf not in clientes_por_agencia[agencia]:
                clientes_por_agencia[agencia].append(cpf)

    # Inicializa variáveis para armazenar a agência com mais clientes e a quantidade máxima de clientes
    melhor_agencia = False
    maior_quantidade = 0

    # Percorre o dicionário de clientes por agência para encontrar a agência com mais clientes
    for agencia in clientes_por_agencia:
        quantidade = len(clientes_por_agencia[agencia])
        if quantidade > maior_quantidade:
            maior_quantidade = quantidade
            melhor_agencia = agencia
    # Retorna a agência com mais clientes ou False se não houver agências
    return melhor_agencia


# Função para contar as contas conjuntas (mais de um titular)
def contar_contas_conjuntas(contas):
    # Inicializa a variável quantidade com 0 para contar as contas conjuntas
    quantidade = 0
    # Percorre a lista de contas e verifica se cada conta tem mais de um cliente (titular)
    for conta in contas:
        if len(conta["clientes"]) > 1:
            quantidade += 1
    # Retorna a quantidade de contas conjuntas encontradas
    return quantidade