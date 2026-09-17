def cadastrar_cliente(clientes, nome_digitado, cpf_digitado):
    clientes.append((nome_digitado, cpf_digitado))


def procurar_cliente(clientes, cpf_digitado):

    for cliente in clientes:

        if cliente[1] == cpf_digitado:

            return cliente


    return None