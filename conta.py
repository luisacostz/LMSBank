def cadastrar_conta(contas, numero_conta, cpfs_vinculados, numero_agencia):
    nova_conta = (numero_conta, cpfs_vinculados, numero_agencia, 0.0)
    contas.append(nova_conta)

def listar_contas(contas):
    print("\n--- Lista de Contas ---")
    for i in range(len(contas)):
        print("Conta:", contas[i][0], "- CPFs vinculados:", contas[i][1], "- Agencia:", contas[i][2], "- Saldo: R$", contas[i][3])

def consultar_saldo(contas, numero_conta):
    for i in range(len(contas)):
        if contas[i][0] == numero_conta:
            print("Saldo atual: R$", contas[i][3])
            return
    print("Conta nao encontrada.")

def depositar(contas, numero_conta, valor):
    for i in range(len(contas)):
        if contas[i][0] == numero_conta:
            if valor > 0:
                conta_atual = contas[i]
                contas[i] = (conta_atual[0], conta_atual[1], conta_atual[2], conta_atual[3] + valor)
                print("Deposito realizado!")
                return
            else:
                print("Valor de deposito invalido!")
                return
    print("Conta nao encontrada.")

def sacar(contas, numero_conta, valor):
    for i in range(len(contas)):
        if contas[i][0] == numero_conta:
            conta_atual = contas[i]
            if conta_atual[3] >= valor and valor > 0:
                contas[i] = (conta_atual[0], conta_atual[1], conta_atual[2], conta_atual[3] - valor)
                print("Saque realizado!")
                return
            else:
                print("Saldo insuficiente ou valor invalido.")
                return
    print("Conta nao encontrada.")

def transferir(contas, numero_origem, numero_destino, valor):
    indice_origem = -1
    indice_destino = -1
    
    for i in range(len(contas)):
        if contas[i][0] == numero_origem:
            indice_origem = i
        if contas[i][0] == numero_destino:
            indice_destino = i
            
    if indice_origem != -1 and indice_destino != -1 and valor > 0:
        conta_origem = contas[indice_origem]
        conta_destino = contas[indice_destino]
        
        if conta_origem[3] >= valor:
            contas[indice_origem] = (conta_origem[0], conta_origem[1], conta_origem[2], conta_origem[3] - valor)
            contas[indice_destino] = (conta_destino[0], conta_destino[1], conta_destino[2], conta_destino[3] + valor)
            print("Transferencia realizada!")
        else:
            print("Saldo insuficiente na conta de origem.")
    else:
        print("Contas invalidas ou valor incorreto.")