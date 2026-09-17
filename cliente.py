def cadastrar_cliente(clientes, nome_digitado, cpf_digitado):
    clientes.append((nome_digitado, cpf_digitado))


def listar_clientes(clientes):
    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
    else:
        print("\n--- LISTA DE CLIENTES ---")
        for cliente in clientes:
            print("Nome:", cliente[0], "- CPF:", cliente[1])
            

def procurar_cliente(clientes, cpf_digitado):
    for cliente in clientes:
        if cliente[1] == cpf_digitado:
            return cliente
    return None
