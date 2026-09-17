from cliente import cadastrar_cliente, procurar_cliente
from conta import consultar_saldo, depositar, sacar, cadastrar_conta
from menu import menu


clientes = []
contas = []
agencias = []


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

            cadastrar_cliente(clientes, nome_digitado, cpf_digitado)

            print("Cliente cadastrado com sucesso!")

        elif opcao == "2":
            numero_conta = input("Digite o número da conta: ")
            cpf_cliente = input("Digite o cpf do cliente: ")

            cliente_encontrado = procurar_cliente(clientes, cpf_cliente)

            if cliente_encontrado != None:
                cadastrar_conta(contas, numero_conta, cpf_cliente)
                print("Conta cadastrada com sucesso!")
            else:
                print("Cliente não encontrado!")

        elif opcao == "3":
            consultar_saldo(saldo_atual)

        elif opcao == "4":
            valor_deposito = float(input("Digite o valor do depósito: "))
            saldo_atual = depositar(saldo_atual, valor_deposito)
            consultar_saldo(saldo_atual)

        elif opcao == "5":
            valor_saque = float(input("Digite o valor do saque: "))
            saldo_atual = sacar(saldo_atual, valor_saque)
            consultar_saldo(saldo_atual)

        elif opcao == "0":
            print("\nAgradecemos por utilizar o LMS Bank!")

        else:
            print("\nOpção inválida! Digite uma opção válida.")


main()