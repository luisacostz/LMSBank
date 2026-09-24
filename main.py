from cliente import cadastrar_cliente, procurar_cliente, listar_clientes
from agencia import cadastrar_agencia, procurar_agencia, listar_agencias
from conta import cadastrar_conta, listar_contas, consultar_saldo, depositar, sacar, transferir, montante_total_banco, montante_total_agencia, procurar_conta
from menu import menu
from armazenamento import salvar_dados, carregar_dados

def main():
    dados_iniciais = carregar_dados()
    clientes = dados_iniciais[0]
    agencias = dados_iniciais[1]
    contas = dados_iniciais[2]

    rodando = True

    while rodando:
        menu()
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            cpf = input("CPF do cliente: ")
            cliente_existente = procurar_cliente(clientes, cpf)
            
            if cliente_existente == False:
                nome = input("Nome do cliente: ")
                data_nascimento = input("Data de nascimento: ")
                email = input("Email: ")
                telefone = input("Telefone: ")
                endereco = input("Endereco: ")
                
                cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco)
                salvar_dados(clientes, agencias, contas)
                print("Cadastrado.")
            else:
                print("Este CPF ja esta no sistema!")
            
        elif opcao == "2":
            listar_clientes(clientes)

        elif opcao == "3":
            cpf_busca = input("CPF do cliente: ")
            cliente_encontrado = procurar_cliente(clientes, cpf_busca)

            if cliente_encontrado != False:
                print("\nDados:")
                print("Nome:", cliente_encontrado[0])
                print("CPF:", cliente_encontrado[1])
                print("Data de Nascimento:", cliente_encontrado[2])
                print("Email:", cliente_encontrado[3])
                print("Telefone:", cliente_encontrado[4])
                print("Endereco:", cliente_encontrado[5])
            else:
                print("Cliente nao encontrado.")
                
        elif opcao == "4":
            numero_agencia = input("Numero da agencia: ")
            agencia_existente = procurar_agencia(agencias, numero_agencia)
            
            if agencia_existente == False: 
                nome_agencia = input("Nome da agencia: ")
                cadastrar_agencia(agencias, numero_agencia, nome_agencia)
                salvar_dados(clientes, agencias, contas)
                print("Cadastrado!")
            else:
                print("Esta agencia ja esta no sistema!")
            
        elif opcao == "5":
            listar_agencias(agencias)
            
        elif opcao == "6":
            agencia_busca = input("Numero da agencia: ")
            agencia_encontrada = procurar_agencia(agencias, agencia_busca)
            
            if agencia_encontrada != False:
                print("Dados:")
                print("Numero:", agencia_encontrada[0])
                print("Nome:", agencia_encontrada[1])
            else:
                print("Agencia nao encontrada.")

        elif opcao == "7":
            numero_conta = input("Numero da conta: ")
            conta_existente = procurar_conta(contas, numero_conta)
            
            if conta_existente == False:
                numero_agencia = input("Numero da agencia: ")
                agencia_encontrada = procurar_agencia(agencias, numero_agencia)
                
                if agencia_encontrada != False:
                    quantidade_titulares = int(input("Quantidade de titulares: "))
                    cpfs_temporarios = []

                    for i in range(quantidade_titulares):
                        cpf = input("CPF do titular: ")
                        cliente_encontrado = procurar_cliente(clientes, cpf)

                        if cliente_encontrado != False:
                            cpfs_temporarios.append(cpf)
                        else:
                            print("Cliente nao encontrado!")

                    if len(cpfs_temporarios) > 0:
                        cpfs_vinculados = tuple(cpfs_temporarios)
                        cadastrar_conta(contas, numero_conta, cpfs_vinculados, numero_agencia)
                        salvar_dados(clientes, agencias, contas)
                        print("Cadastrado!")
                    else:
                        print("Nenhum titular valido.")
                else:
                    print("Agencia nao encontrada.")
            else:
                print("Este numero de conta ja esta no sistema!")

        elif opcao == "8":
            listar_contas(contas)

        elif opcao == "9":
            numero_conta = input("Numero da conta: ")
            consultar_saldo(contas, numero_conta)

        elif opcao == "10":
            numero_conta = input("Numero da conta: ")
            valor = float(input("Valor do deposito: "))
            depositar(contas, numero_conta, valor)
            salvar_dados(clientes, agencias, contas)

        elif opcao == "11":
            numero_conta = input("Numero da conta: ")
            valor = float(input("Valor do saque: "))
            sacar(contas, numero_conta, valor)
            salvar_dados(clientes, agencias, contas)

        elif opcao == "12":
            numero_origem = input("Numero da conta de origem: ")
            numero_destino = input("Numero da conta destino: ")
            valor = float(input("Valor da transferencia: "))
            transferir(contas, numero_origem, numero_destino, valor)
            salvar_dados(clientes, agencias, contas)
                
        elif opcao == "13":
            print("\n--- RELATORIO DO BANCO ---")
            print("Total de Clientes:", len(clientes))
            print("Total de Agencias:", len(agencias))
            print("Total de Contas:", len(contas))
            
        elif opcao == "14":
            numero_agencia = input("Numero da agencia: ")
            montante_total_agencia(contas, numero_agencia)
            
        elif opcao == "15":
            montante_total_banco(contas)
            
        elif opcao == "16":
            salvar_dados(clientes, agencias, contas)
            print("Dados salvos.")

        elif opcao == "0":
            print("\nObrigado. Volte sempre! | LMS Bank.")
            rodando = False

        else:
            print("\nOpcao invalida! Tente novamente.")

main()