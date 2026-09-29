'''
Módulo: agencia.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar e listar agências.
'''

# Função para cadastrar uma nova agência
def cadastrar_agencia(agencias, numero_agencia, nome_agencia):
    # Cria uma tupla representando a nova agência com o número e nome inserdos pelo usuário
    nova_agencia = (numero_agencia, nome_agencia)
    # Adiciona a nova agência à lista de agências
    agencias.append(nova_agencia)

# Função para procurar uma agência pelo número
def procurar_agencia(agencias, numero_procurado):
    # Percorre a lista de agências para encontrar uma agência com o número correspondente
    for i in range(len(agencias)):
        if agencias[i][0] == numero_procurado:
            # Retorna a agência encontrada
            return agencias[i]
    # Se não encontrar a agência, retorna False
    return False

# Função para listar todas as agências cadastradas
def listar_agencias(agencias):
    # Verifica se a lista de agências está vazia
    if len(agencias) == 0:
        print("Nenhuma agencia cadastrada.")
    # Percorre a lista de agências e exibe o número e nome de cada uma
    else:
        print("\n--- LISTA DE AGENCIAS ---")
        for i in range(len(agencias)):
            print("Numero:", agencias[i][0])
            print("Nome:", agencias[i][1])