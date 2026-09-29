'''
Módulo: cliente.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar e listar clientes.
'''

# Função para cadastrar um novo cliente
def cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco):
    # Cria uma tupla representando o novo cliente com os dados fornecidos
    novo_cliente = (nome, cpf, data_nascimento, email, telefone, endereco)
    # Adiciona o novo cliente à lista de clientes
    clientes.append(novo_cliente)

def procurar_cliente(clientes, cpf_busca):
    # Percorre a lista de clientes para encontrar um cliente com o CPF correspondente
    for i in range(len(clientes)):
        # Verifica se o CPF do cliente atual corresponde ao CPF buscado
        if clientes[i][1] == cpf_busca:
            # Retorna o cliente encontrado
            return clientes[i]
    # Se não encontrar o cliente, retorna False
    return False

# Função para listar todos os clientes cadastrados
def listar_clientes(clientes):
    # Verifica se a lista de clientes está vazia
    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
    # Percorre a lista de clientes e exibe os dados de cada um
    else:
        print("\n--- Lista de Clientes ---")
        for i in range(len(clientes)):
            # Armazena o cliente atual numa variável para facilitar a leitura do código
            cliente_atual = clientes[i]
            print("Nome:", cliente_atual[0])
        print("CPF:", cliente_atual[1])
        print("Nascimento:", cliente_atual[2])
        print("Email:", cliente_atual[3])
        print("Telefone:", cliente_atual[4])
        print("Endereco:", cliente_atual[5])
        print("-------------------------")