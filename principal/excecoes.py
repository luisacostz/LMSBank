'''
Módulo: excecoes.py
Descrição: Erros do banco. As classes lançam estas exceções em vez de usar print,
e quem chama (console ou Flask) decide como mostrar a mensagem ao usuário.
'''


class BancoError(Exception):
    '''Erro base do banco'''

class ValorInvalidoError(BancoError):
    '''Valor de depósito, saque ou transferência inválida'''

class SaldoInsuficienteError(BancoError):
    '''O saldo disponível da conta não cobre o valor pedido.'''

class OperacaoInvalidaError(BancoError):
    '''Operação que não faz sentido'''

class TipoContaInvalidoError(BancoError):
    '''Tipo de conta desconhecido'''
