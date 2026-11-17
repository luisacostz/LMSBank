'''
Módulo: menu.py
Autores: Luísa Costa, Murilo Santana e Sarah Beatriz
Descrição: Este módulo contém a função para exibir o menu de opções do programa.
'''

# Exibe o menu principal organizado por categorias (clientes, agência, contas, operações e relatórios)
def menu():
    print("\n--- CLIENTES ---")
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Procurar Cliente por CPF")
    print("--- AGENCIA ---")
    print("4 - Ver dados da Agencia")
    print("--- CONTAS ---")
    print("5 - Cadastrar Conta")
    print("6 - Listar Contas")
    print("7 - Procurar Conta por número")
    print("8 - Procurar Contas por CPF")
    print("--- OPERACOES ---")
    print("9 - Consultar Saldo")
    print("10 - Depositar")
    print("11 - Sacar")
    print("12 - Transferir")
    print("--- RELATORIOS ---")
    print("13 - Montante total do banco")
    print("14 - Contas com saldo positivo")
    print("15 - Conta com maior saldo")
    print("16 - Conta com menor saldo")
    print("17 - Dashboard do banco")
    print("0 - Sair")
