'''
Módulo: cliente.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar e listar clientes.
'''
from principal.cpf import validar_cpf, limpar_cpf


# Função para cadastrar um novo cliente
def cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco):
    # Verifica se o CPF é válido
    if validar_cpf(cpf) == False:
        print("CPF inválido. Cliente não cadastrado.")
        return False

    # Cria um dicionário representando o novo cliente
    novo_cliente = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "email": email,
        "telefone": telefone,
        "endereco": endereco
    }

    # Adiciona o novo cliente à lista
    clientes.append(novo_cliente)

    print("Cliente cadastrado com sucesso.")
    return True
# Função para procurar um cliente pelo CPF
def procurar_cliente(clientes, cpf_busca):
    # Remove a pontuação do CPF pesquisado
    cpf_busca = limpar_cpf(cpf_busca)

    # Percorre a lista de clientes
    for cliente in clientes:
        # Remove a pontuação do CPF cadastrado
        cpf_cliente = limpar_cpf(cliente["cpf"])

        # Compara os CPFs sem pontuação
        if cpf_cliente == cpf_busca:
            return cliente

    # Se não encontrar, retorna False
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