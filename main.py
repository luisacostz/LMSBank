# Arquivo principal do LMS BANK
from cliente import cadastrar_cliente
from conta import consultar_saldo, depositar, sacar

nome = input("Digite seu nome:")
cpf = input("Digite seu cpf:")

nome, cpf = cadastrar_cliente(nome, cpf)
saldo = 0

consultar_saldo(saldo)

valor_deposito = float(input("Digite o valor do depósito:"))


saldo = depositar(saldo,valor_deposito)

consultar_saldo(saldo)

valor_saque = float(input("Digite o valor do saque:"))

saldo = sacar(saldo, valor_saque)

consultar_saldo(saldo)