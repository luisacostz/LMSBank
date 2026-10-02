'''
Módulo: agencia.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar e listar agências.
'''

# Função para cadastrar uma nova agência
def cadastrar_agencia(agencias, numero_agencia, nome, telefone, endereco):
    # Cria um dicionário representando a nova agência com os dados fornecidos
    nova_agencia = {
        "numero_agencia": numero_agencia,
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco
    }
    # Adiciona a nova agência à lista de agências
    agencias.append(nova_agencia)


# Função para procurar uma agência pelo número
def procurar_agencia(agencias, numero_procurado):
    # Percorre a lista de agências para encontrar uma com o número correspondente
    for agencia in agencias:
        if agencia["numero_agencia"] == numero_procurado:
            # Retorna a agência encontrada
            return agencia
    # Se não encontrar a agência, retorna False
    return False


# Função para listar todas as agências cadastradas
def listar_agencias(agencias):
    # Verifica se a lista de agências está vazia
    if len(agencias) == 0:
        print("Nenhuma agencia cadastrada.")
    # Percorre a lista de agências e exibe os dados de cada uma
    else:
        print("\n--- LISTA DE AGENCIAS ---")
        for agencia in agencias:
            print("Número:", agencia["numero_agencia"])
            print("Nome:", agencia["nome"])
            print("Telefone:", agencia["telefone"])
            print("Endereço:", agencia["endereco"])
            print("--------------------------------------")