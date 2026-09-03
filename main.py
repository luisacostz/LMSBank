# Arquivo principal do LMS BANK

from cliente import cadastrar_cliente
from conta import consultar_saldo, depositar, sacar

def menu():
    print("\n-----------------------------------------")
    print("        BEM-VINDO AO LMS BANK           ")
    print("-----------------------------------------")
    print("  [1] Cadastrar um Cliente")
    print("  [2] Consultar saldo")
    print("  [3] Depositar")
    print("  [4] Sacar")
    print("  [0] Sair do sistema")
    print("------------------------------------------")


def main():
    nome_atual = ""
    cpf_atual = ""
    saldo_atual = 0.0

    for funcionamento in range(100):
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_digitado = input("Digite seu nome: ")
            cpf_digitado = input("Digite seu cpf: ")

            nome_atual, cpf_atual = cadastrar_cliente(nome_digitado, cpf_digitado)

            print("Cliente cadastrado com sucesso!")

        elif opcao == "2":
            consultar_saldo(saldo_atual)
        
        elif opcao == "3":
            valor_deposito = float(input("Digite o valor do depósito: "))
            saldo_atual = depositar(saldo_atual, valor_deposito)
            consultar_saldo(saldo_atual)        

        elif opcao == "4":
            valor_saque = float(input("Digite o valor do saque: "))
            saldo_atual = sacar(saldo_atual, valor_saque)
            consultar_saldo(saldo_atual)

        elif opcao == "0":
            print("\nAgradecemos por utilizar o LMS Bank!")
        
        else:
            print("\nOpção inválida! Digite um dos números: 1, 2, 3, 4 ou 0.")

main()