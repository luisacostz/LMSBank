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

    for funcionamento in range(5):
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Cadastrar")
        
        elif opcao == "2":
            print("Saldo")
        
        elif opcao == "3":
            print("Depositar")
        
        elif opcao == "4":
            print("Sacar")
        
        elif opcao == "0":
            print("\nAgradecemos por utilizar o LMS Bank!")
        
        else:
            print("\nOpção inválida! Digite um dos números: 1, 2, 3, 4 ou 0.")

if __name__ == "__main__":
    main()