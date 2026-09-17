def consultar_saldo(saldo_atual):
  print('Seu saldo atual é:' , saldo_atual)
  return saldo_atual

def depositar(saldo_atual, valor_deposito):
  if valor_deposito > 0:
    novo_saldo = saldo_atual + valor_deposito
    return novo_saldo
  else:
    print('Valor inválido')
    return saldo_atual

def sacar(saldo_atual, valor_saque):
  if valor_saque > saldo_atual:
    print('Saldo insufuciente')
    return saldo_atual
  else:
    return saldo_atual - valor_saque

  

def cadastrar_conta(contas, numero_conta, cpf_cliente):

    conta = (numero_conta, cpf_cliente, 0.0)

    contas.append(conta)
