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
    print("3 - Procurar Cliente")

    # Exibe as opções de gestão de agências
    print("--- AGENCIAS ---")
    print("4 - Cadastrar Agencia")
    print("5 - Listar Agencias")
    print("6 - Procurar Agencia")

    # Exibe as opções de gestão de contas
    print("--- CONTAS ---")
    print("7 - Cadastrar Conta")
    print("8 - Listar Contas")

    # Exibe as opções de operações bancárias
    print("--- OPERACOES ---")
    print("9 - Consultar Saldo")
    print("10 - Depositar")
    print("11 - Sacar")
    print("12 - Transferir")

    # Exibe as opções de relatórios, salvamento e fechamento do sistema
    print("--- RELATORIOS E SISTEMA ---")
    print("13 - Relatorio do banco")
    print("14 - Montante total por agencia")
    print("15 - Montante total do banco")
    print("16 - Salvar")
    print("0 - Sair")