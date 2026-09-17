from cliente import cadastrar_cliente, procurar_cliente
from conta import cadastrar_conta, listar_contas, consultar_saldo, depositar, sacar, transferir
from menu import menu
from armazenamento import salvar_dados

def main():
    clientes = []
    contas = []
    agencias = []

    for funcionamento in range(100):
        menu()
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            cadastrar_cliente(clientes, nome, cpf)
            salvar_dados(clientes, contas)
            print("Cliente cadastrado com sucesso!")

        elif opcao == "3":
            cpf_busca = input("Digite o CPF do cliente que deseja procurar: ")
            cliente_encontrado = procurar_cliente(clientes, cpf_busca)

            if cliente_encontrado != None:
                print("Cliente Encontrado!")
                print("Nome:", cliente_encontrado[0], "- CPF:", cliente_encontrado[1])
            else:
                print("Cliente nao cadastrado no sistema.")

        elif opcao == "7":
            numero_conta = input("Digite o numero da conta: ")
            numero_agencia = input("Digite o numero da agencia: ")
            quantidade_titulares = int(input("Quantos titulares a conta tera? "))
            cpfs_temporarios = []

            for i in range(quantidade_titulares):
                cpf = input("Digite o CPF do titular: ")
                cliente_encontrado = procurar_cliente(clientes, cpf)

                if cliente_encontrado != None:
                    cpfs_temporarios.append(cpf)
                else:
                    print("Cliente nao encontrado no sistema!")

            if len(cpfs_temporarios) > 0:
                cpfs_vinculados = tuple(cpfs_temporarios)
                cadastrar_conta(contas, numero_conta, cpfs_vinculados, numero_agencia)
                salvar_dados(clientes, contas)
                print("Conta cadastrada com sucesso!")
            else:
                print("Nenhum titular valido. Conta cancelada.")

        elif opcao == "8":
            listar_contas(contas)

        elif opcao == "9":
            numero_conta = input("Digite o numero da conta: ")
            consultar_saldo(contas, numero_conta)

        elif opcao == "10":
            numero_conta = input("Digite o numero da conta: ")
            valor = float(input("Digite o valor do deposito: "))
            depositar(contas, numero_conta, valor)
            salvar_dados(clientes, contas)

        elif opcao == "11":
            numero_conta = input("Digite o numero da conta: ")
            valor = float(input("Digite o valor do saque: "))
            sacar(contas, numero_conta, valor)
            salvar_dados(clientes, contas)

        elif opcao == "12":
            numero_origem = input("Digite a sua conta (origem): ")
            numero_destino = input("Digite a conta destino: ")
            valor = float(input("Digite o valor da transferencia: "))
            transferir(contas, numero_origem, numero_destino, valor)
            salvar_dados(clientes, contas)

        elif opcao == "0":
            print("\nObrigado por utilizar o LMS Bank!")

        else:
            print("\nOpcao invalida ou modulo em desenvolvimento! Tente novamente.")

main()