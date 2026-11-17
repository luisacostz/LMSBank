'''
Módulo: excecoes.py
Descrição: Erros do banco. As classes lançam estas exceções em vez de usar print,
e quem chama (console ou Flask) decide como mostrar a mensagem ao usuário.
'''

# Exceção base para todos os erros específicos do sistema bancário
class BancoError(Exception):
    '''Erro base do banco'''


# Lançada quando o valor informado para movimentação é negativo ou zero
class ValorInvalidoError(BancoError):
    '''Valor de depósito, saque ou transferência inválida'''


# Lançada quando a conta não possui saldo (ou limite) suficiente para a operação
class SaldoInsuficienteError(BancoError):
    '''O saldo disponível da conta não cobre o valor pedido.'''


# Lançada quando uma operação não é permitida (ex: transferir para a mesma conta)
class OperacaoInvalidaError(BancoError):
    '''Operação que não faz sentido'''


# Lançada quando o tipo de conta informado não corresponde aos tipos válidos
class TipoContaInvalidoError(BancoError):
    '''Tipo de conta desconhecido'''


# Lançada quando o CPF informado não atende às regras de validação
class CpfInvalidoError(BancoError):
    pass
