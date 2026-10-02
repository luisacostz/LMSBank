'''
Módulo: main.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém a função principal do programa, que é responsável por exibir o menu e chamar as funções dos outros módulos de acordo com a escolha do usuário.
'''

# Importa as funções dos módulos cliente, agencia, conta, menu, armazenamento e relatorio
from cliente import cadastrar_cliente, procurar_cliente, listar_clientes
from agencia import cadastrar_agencia, procurar_agencia, listar_agencias
from conta import cadastrar_conta, listar_contas, consultar_saldo, depositar, sacar, transferir, procurar_conta, buscar_contas_por_cpf
from menu import menu
from armazenamento import salvar_dados, carregar_dados
from relatorio import montante_total_banco, montante_por_agencia, agencia_mais_clientes, contar_contas_conjuntas

# Função principal do programa
def main():
    # Carrega os dados iniciais do sistema (clientes, agências e contas) a partir do armazenamento
    dados_iniciais = carregar_dados()
    clientes = dados_iniciais[0]
    agencias = dados_iniciais[1]
    contas = dados_iniciais[2]

    rodando = True

    # Loop principal do programa, que exibe o menu e processa as opções escolhidas pelo usuário
    while rodando:
        # Exibe o menu de opções do programa
        menu()
        opcao = input("Escolha uma opcao: ")

        # Processa a opção escolhida pelo usuário e chama as funções correspondentes dos módulos importados
        # 1 - Cadastrar cliente
        if opcao == "1":
            # Solicita ao usuário o CPF do cliente e verifica se ele já está cadastrado
            cpf = input("CPF do cliente: ")
            cliente_existente = procurar_cliente(clientes, cpf)

            # Se o cliente não estiver cadastrado, solicita os dados restantes e chama a função para cadastrar o cliente
            if cliente_existente == False:
                nome = input("Nome do cliente: ")
                data_nascimento = input("Data de nascimento: ")
                email = input("Email: ")
                telefone = input("Telefone: ")
                endereco = input("Endereco: ")
                
                cadastrar_cliente(clientes, nome, cpf, data_nascimento, email, telefone, endereco)
                # Salva os dados atualizados no armazenamento
                salvar_dados(clientes, agencias, contas)
                print("Cadastrado.")
            else:
                print("Este CPF ja esta no sistema!")

        # 2 - Listar clientes    
        elif opcao == "2":
            # Chama a função para listar todos os clientes cadastrados no sistema
            listar_clientes(clientes)

        # 3 - Procurar cliente
        elif opcao == "3":
            # Solicita ao usuário o CPF do cliente que deseja procurar e chama a função correspondente
            cpf_busca = input("CPF do cliente: ")
            cliente_encontrado = procurar_cliente(clientes, cpf_busca)
            
            # Verifica se o cliente foi encontrado e exibe os dados correspondentes ou uma mensagem de erro
            if cliente_encontrado:
                print("\nDados:")
                print("Nome:", cliente_encontrado["nome"])
                print("CPF:", cliente_encontrado["cpf"])
                print("Data de Nascimento:", cliente_encontrado["data_nascimento"])
                print("Email:", cliente_encontrado["email"])
                print("Telefone:", cliente_encontrado["telefone"])
                print("Endereco:", cliente_encontrado["endereco"])
            else:
                print("\nCliente não encontrado.")

        # 4 - Cadastrar agência        
        elif opcao == "4":
            # Solicita ao usuário o número da agência que deseja cadastrar e verifica se ela já está cadastrada
            numero_agencia = input("Número da agência: ")
            agencia_existente = procurar_agencia(agencias, numero_agencia)

            # Se a agência não estiver cadastrada, solicita o nome da agência e chama a função para cadastrá-la
            if agencia_existente == False: 
                nome_agencia = input("Nome da agencia: ")
                telefone_agencia = input("Telefone da agência: ")
                endereco_agencia = input("Endereço da agência: ")
                cadastrar_agencia(agencias, numero_agencia, nome_agencia, telefone_agencia, endereco_agencia)
                salvar_dados(clientes, agencias, contas)
                print("Cadastrado com sucesso!")
            # Se a agência já estiver cadastrada, exibe uma mensagem de erro    
            else:
                print("Esta agencia ja esta no sistema!")

        # 5 - Listar agências    
        elif opcao == "5":
            # Chama a função para listar todas as agências cadastradas no sistema
            listar_agencias(agencias)

        # 6 - Procurar agência    
        elif opcao == "6":
            # Solicita ao utilizador o número da agência que deseja procurar
            agencia_busca = input("Número da agência: ")
            agencia_encontrada = procurar_agencia(agencias, agencia_busca)

            # Verifica se a agência possui dados válidos
            if agencia_encontrada:
                print("\nDados:")
                print("Numero:", agencia_encontrada["numero_agencia"])
                print("Nome:", agencia_encontrada["nome"])
                print("Telefone:", agencia_encontrada["telefone"])
                print("Endereco:", agencia_encontrada["endereco"])
            else:
                print("\nAgência não encontrada.")

        # 7 - Cadastrar conta
        elif opcao == "7":
            numero_conta = input("Numero da conta: ")
            conta_existente = procurar_conta(contas, numero_conta)
 
            if conta_existente == False:
                numero_agencia = input("Numero da agencia: ")
                agencia_encontrada = procurar_agencia(agencias, numero_agencia)
 
                if agencia_encontrada:
                    # >>> TIPO DE CONTA <<<
                    texto_quantidade = input("Quantidade de titulares: ")
 
                    # Só aceita se for um número inteiro maior que zero
                    if int(texto_quantidade) < 1:
                        print("Quantidade de titulares inválida.")
                    else:
                        quantidade_titulares = int(texto_quantidade)
                        # Lista para armazenar os CPFs vinculados à conta
                        cpfs_vinculados = []
                        cancelado = False
 
                        # Repete até completar a quantidade de titulares
                        while len(cpfs_vinculados) < quantidade_titulares and cancelado == False:
                            # Solicita ao usuário o CPF do titular da conta e verifica se ele é válido e não está duplicado
                            cpf = input(f"CPF do titular {len(cpfs_vinculados) + 1} (Enter para cancelar): ")

                            # Se for um input vazio, cancela o cadastro da conta
                            if cpf == "":
                                cancelado = True
                            # Se o cliente não estiver cadastrado, exibe uma mensagem de erro
                            elif procurar_cliente(clientes, cpf) == False:
                                print("Cliente não encontrado!")
                            # Se o CPF já estiver vinculado à conta, exibe uma mensagem de erro
                            elif cpf in cpfs_vinculados:
                                print("Este CPF já é titular desta conta!")
                            # Se o CPF for válido e não estiver duplicado, adiciona à lista de CPFs vinculados à conta
                            else:
                                cpfs_vinculados.append(cpf)
                        # Se o cadastro da conta não foi cancelado, chama a função para cadastrar a conta e salva os dados atualizados no armazenamento
                        if cancelado:
                            print("Cadastro de conta cancelado.")
                        # Se o cadastro da conta não foi cancelado, chama a função para cadastrar a conta e salva os dados atualizados no armazenamento
                        else:
                            cadastrar_conta(contas, numero_conta, cpfs_vinculados, numero_agencia)
                            salvar_dados(clientes, agencias, contas)
                            print("Cadastrado!")
                # Se a agência não for encontrada, exibe uma mensagem de erro
                else:
                    print("Agencia nao encontrada.")
            # Se a conta já estiver cadastrada, exibe uma mensagem de erro
            else:
                print("Este numero de conta ja esta no sistema!")


        # 8 - Listar contas
        elif opcao == "8":
            # Chama a função para listar todas as contas cadastradas no sistema
            listar_contas(contas)


        # 9 - Procurar conta por número da conta
        elif opcao == "9":
            # Solicita ao usuário o número da conta que deseja procurar e chama a função de procurar a conta
            numero_conta = input("Numero da conta: ")
            conta_encontrada = procurar_conta(contas, numero_conta)

            # Verifica se a conta foi encontrada e chama a função de listar contas para exibir os dados da conta encontrada, ou exibe uma mensagem de erro caso não seja encontrada
            if conta_encontrada:
                listar_contas([conta_encontrada])
            else:
                print("\nConta não encontrada.")


         # 10 - Procurar conta por CPF do titular da conta
        elif opcao == "10":
            # Solicita ao usuário o CPF do titular da conta que deseja procurar e chama a função de buscar contas por CPF
            cpf_busca = input("CPF do titular: ")
            contas_do_cliente = buscar_contas_por_cpf(contas, cpf_busca)

            # Verifica se foram encontradas contas para o CPF fornecido e chama a função de listar contas para exibir os dados das contas encontradas, ou exibe uma mensagem de erro caso não sejam encontradas
            if len(contas_do_cliente) > 0:
                listar_contas(contas_do_cliente)
            else:
                print("\nNenhuma conta encontrada para este CPF.")

        # 11 - Consultar saldo
        elif opcao == "11":
            # Solicita ao usuário o número da conta que deseja consultar e chama a função de consultar o saldo
            numero_conta = input("Numero da conta: ")
            consultar_saldo(contas, numero_conta)

        # 12 - Depositar
        elif opcao == "12":
            # Solicita ao usuário o número da conta e o valor do depósito, e chama a função de depositar
            numero_conta = input("Numero da conta: ")
            valor = float(input("Valor do deposito: "))
            # Chama a função de depositar para realizar o depósito na conta especificada
            depositar(contas, numero_conta, valor)
            # Salva os dados atualizados no armazenamento
            salvar_dados(clientes, agencias, contas)

        # 13 - Sacar
        elif opcao == "13":
            # Solicita ao usuário o número da conta e o valor do saque, e chama a função de sacar
            numero_conta = input("Numero da conta: ")
            valor = float(input("Valor do saque: "))
            sacar(contas, numero_conta, valor)
            # Salva os dados atualizados no armazenamento
            salvar_dados(clientes, agencias, contas)

        # 14 - Transferir
        elif opcao == "14":
            # Solicita ao usuário os números das contas de origem e destino, e o valor da transferência, e chama a função de transferir
            numero_origem = input("Numero da conta de origem: ")
            numero_destino = input("Numero da conta destino: ")
            valor = float(input("Valor da transferencia: "))
            transferir(contas, numero_origem, numero_destino, valor)
            # Salva os dados atualizados no armazenamento
            salvar_dados(clientes, agencias, contas)

        # 15 - Montante total do banco
        elif opcao == "15":
            # Chama a função que calcula o montante total do banco e exibe o resultado
            print("\n--- RELATORIO DO BANCO ---")
            total = montante_total_banco(contas)
            print(f"\nO montante total do banco é: R$ {total:.2f}\n")

        # 16 - Montante total por agência    
        elif opcao == "16":
            # Pede ao usuário qual agência ele quer consultar
            numero_agencia = input("Digite o número da agência para o relatório: ")
            # Chama a função passando a lista de contas e a agência escolhida
            total_agencia = montante_por_agencia(contas, numero_agencia)
            print(f"\nO montante da agência {numero_agencia} é: R$ {total_agencia:.2f}\n")

        # 17 - Agência com mais clientes
        elif opcao == "17":
            # Chama a função que encontra a agência com mais clientes e exibe o resultado
            melhor_agencia = agencia_mais_clientes(contas)
            # Verifica se a função retornou uma agência válida antes de exibir o resultado
            if melhor_agencia:
                print(f"\nA agência com mais clientes é: {melhor_agencia}\n")
            else:
                print("\nNenhuma agência encontrada.\n")

        # 18 - Quantidade de contas conjuntas
        elif opcao == "18":
            print(f"\nQuantidade de contas conjuntas: {contar_contas_conjuntas(contas)}\n")

        # 19 - Salvar
        elif opcao == "19":
            # Salva os dados do sistema (clientes, agências e contas) no armazenamento 
            # O salvamento já é feito a cada operação, mas não sabemos se é melhor assim ou dessa forma
            print("\nSalvando dados do sistema...\n")
            salvar_dados(clientes, agencias, contas)
            print("Dados salvos.")

        # 0 - Sair
        elif opcao == "0":
            print("\nObrigado. Volte sempre! | LMS Bank.")
            # Define a variável 'rodando' como False para encerrar o loop principal e sair do programa
            rodando = False

        # Caso o usuário digite uma opção inválida, exibe uma mensagem de erro
        else:
            print("\nOpção inválida! Tente novamente.")

main()