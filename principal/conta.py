'''
Módulo: conta.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar, listar contas e realizar operações bancárias (como consultar saldo, depositar, sacar e transferir).
'''

# Função para cadastrar uma nova conta no banco
def cadastrar_conta(contas,numero, cliente_infomacao, numero_agencia):
    #tipo = tipo.strip().lower()
    
    # Cria um dicionário para representar a conta 
    nova_conta = {
        "numero": numero,
        # Salva a lista de CPFs para contas conjuntas
        "clientes": cliente_infomacao,
        "agencia": numero_agencia, 
        "saldo": 0.0,
       # "tipo": tipo
    }

    '''
    # Atributos específicos de cada conta
    if tipo == "corrente":
        nova_conta["limite"] = 500.0 # cheque especial
    elif tipo == "poupanca":
        nova_conta["taxa_rendimento"] = 0.01 # rendimento de 1%
    elif tipo == "salario":
        nova_conta["empregador"] = empregador  # Nome do empregador
    else:
        return False
    '''
    # Adiciona a nova conta à lista do banco                                     
    contas.append(nova_conta)
    return True

# Função para listar todas as contas cadastradas no banco
def listar_contas(contas):
    print("\nLista de Contas:")
    for conta in contas:
        print(f"Conta: {conta['numero']}")
        # Une todos os CPFs vinculados à conta separados por vírgula
        cpfs_formatados = ", ".join(conta["clientes"])
        print(f"CPFs: {cpfs_formatados}")
        print(f"Agência: {conta['agencia']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("------------------------")


# Função para procurar uma conta pelo número
def procurar_conta(contas, numero_conta):
    for conta in contas:
        # Verifica se o número da conta corresponde ao número fornecido e retorna a conta encontrada
        if conta["numero"] == numero_conta:
            return conta
    return False

# Função para buscar todas as contas em que um CPF é titular
def buscar_contas_por_cpf(contas, cpf):
    encontradas = []
    for conta in contas:
        if cpf in conta["clientes"]:
            encontradas.append(conta)
    return encontradas


# Função para consultar o saldo de uma conta específica
def consultar_saldo(contas, numero_conta):
    for conta in contas:
        # Verifica se o número da conta corresponde ao número fornecido e exibe o saldo atual
        if conta["numero"] == numero_conta:
            print(f"Saldo atual: R$ {conta['saldo']:.2f}")
            return
    # Se a conta não for encontrada, exibe uma mensagem de erro    
    print("Conta não encontrada.")


# Função para depositar um valor em uma conta específica
def depositar(contas, numero_conta, valor):
    # Percorre a lista de contas para encontrar a conta correspondente ao número fornecido
    for conta in contas:
        if conta["numero"] == numero_conta:
            # Verifica se o valor do depósito é positivo antes de realizar a operação
            if valor > 0:
                # Atualiza o saldo da conta adicionando o valor do depósito e exibe uma mensagem de sucesso
                conta["saldo"] += valor
                print(f"Depósito de R${valor:.2f} realizado na conta {numero_conta}.")
            # Caso contrário, exibe uma mensagem de erro indicando que o valor do depósito deve ser positivo
            else:
                print("O valor do depósito deve ser positivo.")
            return 
    # Se a conta não for encontrada, exibe uma mensagem de erro
    print("Conta não encontrada para depósito.")


# Função para sacar um valor de uma conta específica
def sacar(contas, numero_conta, valor):
    # Percorre a lista de contas para encontrar a conta correspondente ao número fornecido
    for conta in contas:
        if conta["numero"] == numero_conta:
            # Verifica se o valor do saque é positivo e se há saldo suficiente na conta
            if valor > 0 and conta["saldo"] >= valor:
                # Atualiza o saldo da conta subtraindo o valor do saque e exibe uma mensagem de sucesso
                conta["saldo"] -= valor
                print(f"Saque de R${valor:.2f} realizado na conta {numero_conta}.")
            # Caso contrário, exibe uma mensagem de erro
            else:
                print("Saldo insuficiente ou valor de saque inválido.")
            return 
    # Se a conta não for encontrada, exibe uma mensagem de erro
    print("Conta não encontrada para saque.")


# Função para transferir um valor de uma conta para outra
def transferir(contas, numero_origem, numero_destino, valor):
    # Reutiliza a lógica existente para encontrar os dicionários de cada conta
    conta_origem = procurar_conta(contas, numero_origem)
    conta_destino = procurar_conta(contas, numero_destino)

    # Verifica se ambas as contas existem e o valor da transferência é positivo
    if conta_origem and conta_destino and valor > 0:
        # Verifica se a conta de origem tem saldo suficiente
        if conta_origem["saldo"] >= valor:
            # Corrigido: atualiza o saldo diretamente nos dicionários originais
            conta_origem["saldo"] -= valor
            conta_destino["saldo"] += valor
            print("Transferência realizada com sucesso!")
        else:
            print("Saldo insuficiente na conta de origem.")
    else:
        print("Contas inválidas ou valor incorreto.")
