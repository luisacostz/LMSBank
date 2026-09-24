def cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco):
    novo_cliente = (nome, cpf, data_nascimento, email, telefone, endereco)
    clientes.append(novo_cliente)

def procurar_cliente(clientes, cpf_busca):
    for i in range(len(clientes)):
        if clientes[i][1] == cpf_busca:
            return clientes[i]
    return False

def listar_clientes(clientes):
    print("\n--- Lista de Clientes ---")
    for i in range(len(clientes)):
        cliente_atual = clientes[i]
        print("Nome:", cliente_atual[0])
        print("CPF:", cliente_atual[1])
        print("Nascimento:", cliente_atual[2])
        print("Email:", cliente_atual[3])
        print("Telefone:", cliente_atual[4])
        print("Endereco:", cliente_atual[5])
        print("-------------------------")