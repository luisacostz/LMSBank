from cliente import cadastrar_cliente, procurar_cliente
from conta import cadastrar_conta, listar_contas, consultar_saldo, depositar, sacar, transferir
from agencia import cadastrar_agencia, listar_agencias, procurar_agencia
from menu import menu
from armazenamento import salvar_dados

def main():
    clientes = []
    contas = []
    agencias = []

    while rodando:
        menu()
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            cadastrar_cliente(clientes, nome, cpf)
            salvar_dados(clientes, contas)
            print("Cliente cadastrado com sucesso!")

        elif opcao == "2":
            listar_clientes(clientes)

        elif opcao == "3":
            cpf_busca = input("Digite o CPF do cliente que deseja procurar: ")
            cliente_encontrado = procurar_cliente(clientes, cpf_busca)

            if cliente_encontrado != None:
                print("Cliente Encontrado!")
                print("Nome:", cliente_encontrado[0], "- CPF:", cliente_encontrado[1])
            else:
                print("Cliente nao cadastrado no sistema.")

        elif opcao == "4":
            numero_ag = input("Digite o número da agência: ")
            nome_ag = input("Digite o nome da agência: ")
            cadastrar_agencia(agencias, numero_ag, nome_ag)
            salvar_dados(clientes, contas, agencias)

        elif opcao == "5":
            listar_agencias(agencias)

        elif opcao == "6":
            numero_busca = input("Digite o número da agência que deseja procurar: ")
            agencia_encontrada = procurar_agencia(agencias, numero_busca)
            if agencia_encontrada != None:
                print("Agência Encontrada!")
                print("Número:", agencia_encontrada[0], "- Nome:", agencia_encontrada[1])
            else:
                print("Agência não cadastrada no sistema.")


        elif opcao == "7":
            numero_conta = input("Digite o numero da conta: ")
            numero_agencia = input("Digite o numero da agencia: ")
            agenciai_valida = procurar_agencia(agencias, numero_agencia)
            if agencia_valida == None:
                print('Agência não encontrada! Cadastre a agência.')
            else:
                quantidade_titulares = int(input("Quantos titulares a conta tera? "))
                cpfs_temporarios = []
                for i in range(quantidade_titulares):
                    cpf = input("Digite o CPF do titular: ")
                    clientte_encontrado = procurar_cliente(clientes, cpf)
                    if cliente_encontrado != None:
                        cpfs_temporarios.append(cpf):
                    else:
                        print("Cliente não encontrado no sistema!")

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
            salvar_dados(clientes, contas, agencias)

        elif opcao == "11":
            numero_conta = input("Digite o numero da conta: ")
            valor = float(input("Digite o valor do saque: "))
            sacar(contas, numero_conta, valor)
            salvar_dados(clientes, contas, agencias)

        elif opcao == "12":
            numero_origem = input("Digite a sua conta (origem): ")
            numero_destino = input("Digite a conta destino: ")
            valor = float(input("Digite o valor da transferencia: "))
            transferir(contas, numero_origem, numero_destino, valor)
            salvar_dados(clientes, contas, agencias)

        elif opcao == "0":
            print("\nObrigado por utilizar o LMS Bank!")
            rodando = False

        else:
            print("\nOpcao invalida ou modulo em desenvolvimento! Tente novamente.")
            

main()
