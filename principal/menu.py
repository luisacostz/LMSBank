'''
Módulo: menu.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém a função para exibir o menu de opções do programa.
'''

# Função para exibir o menu de opções do programa
def menu():
    # Exibe as opções de gestão de clientes
    print("\n--- CLIENTES ---")
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Procurar Cliente (por CPF)")

    # Exibe as opções de gestão de agências
    print("--- AGENCIAS ---")
    print("4 - Cadastrar Agencia")
    print("5 - Listar Agencias")
    print("6 - Procurar Agencia")

    # Exibe as opções de gestão de contas
    print("--- CONTAS ---")
    print("7 - Cadastrar Conta")
    print("8 - Listar Contas")
    print("9 - Procurar Conta (por número)")
    print("10 - Procurar Contas (por CPF)")

    # Exibe as opções de operações bancárias
    print("--- OPERACOES ---")
    print("11 - Consultar Saldo")
    print("12 - Depositar")
    print("13 - Sacar")
    print("14 - Transferir")

    # Exibe as opções de relatórios, salvamento e fechamento do sistema
    print("--- RELATÓRIOS E SISTEMA ---")
    print("15 - Montante total do banco")
    print("16 - Montante total por agência")
    print("17 - Agência com mais clientes")
    print("18 - Quantidade de contas conjuntas")
    print("19 - Salvar")
    print("0 - Sair")