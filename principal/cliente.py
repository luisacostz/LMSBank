'''
Módulo: cliente.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar e listar clientes.
'''

# Função para cadastrar um novo cliente
def cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco):
    # Cria um dicionário representando o novo cliente com os dados fornecidos
    novo_cliente = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "email": email,
        "telefone": telefone,
        "endereco": endereco
    }
    # Adiciona o novo cliente à lista de clientes
    clientes.append(novo_cliente)

# Função para procurar um cliente pelo CPF
def procurar_cliente(clientes, cpf_busca):
    # Percorre a lista de clientes para encontrar um cliente com o CPF correspondente
    for cliente in clientes:
        # Acesso em O(1) pelo nome da chave correspondente
        if cliente["cpf"] == cpf_busca:
            # Se encontrar o cliente, retorna o dicionário do cliente
            return cliente
    # Se não encontrar o cliente, retorna False
    return False


# Função para listar todos os clientes cadastrados
def listar_clientes(clientes):
    # Verifica se a lista de clientes está vazia
    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
    else:
         # Percorre a lista de clientes e imprime os dados de cada um
        print("\n--- Lista de Clientes ---")
        for cliente in clientes:
            print("Nome:", cliente["nome"])
            print("CPF:", cliente["cpf"])
            print("Nascimento:", cliente["data_nascimento"])
            print("Email:", cliente["email"])
            print("Telefone:", cliente["telefone"])
            print("Endereco:", cliente["endereco"])
            print("-------------------------")