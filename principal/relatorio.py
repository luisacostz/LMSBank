"""
Módulo: relatorio.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para gerar relatórios sobre o banco, como calcular o montante total, montante por agência, agência com mais clientes e quantidade de contas conjuntas.
"""

# Função para calcular o montante total do banco
def montante_total_banco(contas):
    # Soma os saldos de todas as contas no banco.
    total = sum(conta.get('saldo', 0.0) for conta in contas)
    return total


# Função para calcular o montante total de uma agência específica
def montante_por_agencia(contas, numero_agencia):
    # Soma os saldos de todas as contas que pertencem à agência especificada.
    total_agencia = sum(conta.get('saldo', 0.0) for conta in contas if conta.get('agencia') == numero_agencia)
    return total_agencia


# Função para encontrar a agência com mais clientes
def agencia_mais_clientes(contas):
    contagem = {}
    # Conta o número de contas por agência
    for conta in contas:
        agencia = conta.get('agencia')
        if agencia in contagem:
            contagem[agencia] += 1
        else:
            contagem[agencia] = 1
            
    # Se não houver agências, retorna False
    if not contagem:
        return "Nenhuma conta cadastrada"
    # Encontra a agência com o maior número de contas
    melhor_agencia = max(contagem, key=contagem.get)
    return melhor_agencia