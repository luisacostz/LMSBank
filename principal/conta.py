'''
Módulo: conta.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém funções para cadastrar, procurar, listar contas e realizar operações bancárias (como consultar saldo, depositar, sacar e transferir).
'''

# Função para cadastrar uma nova conta no banco
def cadastrar_conta(contas,numero, cliente_infomacao, numero_agencia, tipo, empregador=""):
    tipo = tipo.strip().lower()
    
    # Cria um dicionário para representar a conta 
    nova_conta = {
        "numero": numero,
        # Salva a lista de CPFs para contas conjuntas
        "clientes": cliente_infomacao,
        "agencia": numero_agencia, 
        "saldo": 0.0,
        "tipo": tipo
    }

    
    # Atributos específicos de cada conta
    if tipo == "corrente":
        nova_conta["limite"] = 500.0 # cheque especial
    elif tipo == "poupanca":
        nova_conta["taxa_rendimento"] = 0.01 # rendimento de 1%
    elif tipo == "salario":
        nova_conta["empregador"] = empregador if empregador else ""  # Nome do empregador
    
    # Adiciona a nova conta à lista do banco                                     
    contas.append(nova_conta)

# Função para listar todas as contas cadastradas no banco
def listar_contas(contas):
    print("\nLista de Contas:")
    for conta in contas:
        print(f"Conta: {conta['numero']}")
        print(f"Tipo: {conta.get('tipo', 'corrente').capitalize()}")
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
            print(f"Tipo: {conta['tipo'].capitalize()}")
            print(f"Saldo atual: R$ {conta['saldo']:.2f}")
            if conta["tipo"] == "corrente":
                print(f"Cheque especial: R$ {conta.get('limite', 0.0):.2f}")
                print(f"Saldo total disponível: R$ {(conta['saldo'] + conta.get('limite', 0.0)):.2f}")
            return
    # Se a conta não for encontrada, exibe uma mensagem de erro    
    print("Conta não encontrada.")


# Função para depositar um valor em uma conta específica
def depositar(contas, numero_conta, valor, depositante=""):
    # Percorre a lista de contas para encontrar a conta correspondente ao número fornecido
    for conta in contas:
        if conta["numero"] == numero_conta:
            if valor <= 0:
                print("O valor do depósito deve ser positivo.")
                return

            # Regra para conta salário: só o empregador pode depositar
            if conta["tipo"] == "salario":
                if depositante != conta.get("empregador"):
                    print("Depósito recusado: conta salário só aceita depósitos do empregador cadastrado.")
                    return

            conta["saldo"] += valor
            print(f"Depósito de R${valor:.2f} realizado na conta {numero_conta}.")
            return 
    # Se a conta não for encontrada, exibe uma mensagem de erro
    print("Conta não encontrada para depósito.")


# Função para sacar um valor de uma conta específica
def sacar(contas, numero_conta, valor):
    for conta in contas:
        if conta["numero"] == numero_conta:
            if valor <= 0:
                print("O valor do saque deve ser positivo.")
                return

            # Limite disponível varia de acordo com o tipo
            saldo_disponivel = conta["saldo"]
            if conta["tipo"] == "corrente":
                saldo_disponivel += conta.get("limite", 0.0)

            if saldo_disponivel >= valor:
                conta["saldo"] -= valor
                print(f"Saque de R${valor:.2f} realizado na conta {numero_conta}.")
            else:
                print("Saldo insuficiente para realizar o saque.")
            return
    # Se a conta não for encontrada, exibe uma mensagem de erro
    print("Conta não encontrada para saque.")


# Função para a poupança
def aplicar_rendimento(contas, numero_conta):
    conta = procurar_conta(contas, numero_conta)
    if conta:
        if conta["tipo"] == "poupanca":
            ganho = conta["saldo"] * conta.get("taxa_rendimento", 0.01)
            conta["saldo"] += ganho
            print(f"Rendimento de R${ganho:.2f} creditado na conta {numero_conta}!")
        else:
            print("Operação inválida: esta conta não é poupança.")
    else:
        print("Conta não encontrada.")


# Função para transferir um valor de uma conta para outra
def transferir(contas, numero_origem, numero_destino, valor):
    # Reutiliza a lógica existente para encontrar os dicionários de cada conta
    conta_origem = procurar_conta(contas, numero_origem)
    conta_destino = procurar_conta(contas, numero_destino)

    # Verifica se ambas as contas existem e o valor da transferência é positivo
    if conta_origem and conta_destino and valor > 0:
        # Conta salário não transfere para fora
        if conta_origem.get("tipo") == "salario":
            print("Operação não permitida: conta salário não realiza transferências.")
            return

        # Considera o limite se for corrente
        saldo_disponivel = conta_origem["saldo"]
        if conta_origem.get("tipo") == "corrente":
            saldo_disponivel += conta_origem.get("limite", 0.0)

        if saldo_disponivel >= valor:
            conta_origem["saldo"] -= valor
            conta_destino["saldo"] += valor
            print("Transferência realizada com sucesso!")
        else:
            print("Saldo insuficiente na conta de origem.")
    else:
        print("Contas inválidas ou valor incorreto.")