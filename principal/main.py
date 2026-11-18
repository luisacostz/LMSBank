"""
Módulo: main.py
Descrição: Ponto de entrada da aplicação via console, gerenciando o menu interativo, entrada de dados e chamadas às operações do banco.
"""

# Importa as classes principais do domínio, fábrica de contas, validadores, exceções e o menu
from banco import Banco
from cliente import Cliente
from conta_factory import ContaFactory
from cpf import limpar_cpf, validar_cpf
from excecoes import BancoError, OperacaoInvalidaError, ValorInvalidoError
from menu import menu

# Mapeia as opções numéricas do console para os tipos internos de conta e seus nomes de exibição
TIPOS_CONTA = {"1": "corrente", "2": "poupanca"}
NOMES_TIPO = {"corrente": "Corrente", "poupanca": "Poupança"}


# Retorna a agência única do banco ou lança erro caso não esteja cadastrada
def obter_agencia(banco):
    if banco.agencia is None:
        raise OperacaoInvalidaError("O banco não tem agência cadastrada.")
    return banco.agencia


# Busca um cliente pelo CPF ou lança erro caso não exista
def obter_cliente(banco, cpf):
    cliente = banco.procurar_cliente(cpf)
    if cliente is None:
        raise OperacaoInvalidaError("Cliente não encontrado.")
    return cliente


# Busca uma conta pelo número ou lança erro caso não exista
def obter_conta(banco, numero):
    conta = banco.procurar_conta(numero)
    if conta is None:
        raise OperacaoInvalidaError("Conta não encontrada.")
    return conta


# Lê um valor monetário do teclado e converte para float
def ler_valor(rotulo):
    texto = input(rotulo).strip().replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        raise ValorInvalidoError("Valor inválido! Digite apenas números.")


# Exibe no console os dados completos de um cliente
def exibir_cliente(cliente):
    print(f"Nome: {cliente.nome}")
    print(f"CPF: {cliente.cpf}")
    print(f"Data de Nascimento: {cliente.data_nascimento}")
    print(f"Email: {cliente.email}")
    print(f"Telefone: {cliente.telefone}")
    print(f"Endereco: {cliente.endereco}")
    print(f"Contas: {len(cliente.contas)}")
    print(f"Saldo total: R$ {cliente.saldo_total():.2f}")


# Exibe no console o resumo de uma conta
def exibir_conta(conta):
    titular = conta.cliente.nome if conta.cliente else "-"
    tipo = NOMES_TIPO.get(conta.tipo(), conta.tipo())
    print(f"Conta {conta.numero} | {tipo} | Titular: {titular} | Saldo: R$ {conta.saldo:.2f}")


# Solicita os dados, valida o CPF e cadastra um novo cliente no banco
def cadastrar_cliente(banco):
    cpf = limpar_cpf(input("CPF do cliente: "))
    if not validar_cpf(cpf):
        print("CPF inválido! Precisa ter 11 números e os 2 últimos dígitos (verificadores) corretos.")
        return
    if banco.procurar_cliente(cpf) is not None:
        print("Este CPF já está cadastrado no sistema!")
        return
    nome = input("Nome do cliente: ")
    data_nascimento = input("Data de nascimento: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    endereco = input("Endereco: ")
    cliente = Cliente(nome=nome, cpf=cpf, data_nascimento=data_nascimento,
                      email=email, telefone=telefone, endereco=endereco)
    banco.cadastrar_cliente(cliente)
    print("Cliente cadastrado com sucesso!")


# Lista todos os clientes cadastrados no banco
def listar_clientes(banco):
    if not banco.clientes:
        print("\nNenhum cliente cadastrado.")
        return
    print("\n--- CLIENTES ---")
    for cliente in banco.clientes:
        print(f"{cliente.nome} | CPF: {cliente.cpf} | Contas: {len(cliente.contas)} | Saldo total: R$ {cliente.saldo_total():.2f}")


# Consulta e exibe os dados de um cliente a partir do CPF
def procurar_cliente(banco):
    cpf = limpar_cpf(input("CPF do cliente: "))
    cliente = obter_cliente(banco, cpf)
    print("\nDados:")
    exibir_cliente(cliente)


# Exibe os dados cadastrais e o montante total da agência única do banco
def ver_agencia(banco):
    agencia = obter_agencia(banco)
    print("\nDados:")
    print(f"Numero: {agencia.numero_agencia}")
    print(f"Nome: {agencia.nome}")
    print(f"Telefone: {agencia.telefone}")
    print(f"Endereco: {agencia.endereco}")
    print(f"Contas: {len(agencia.listar_contas())}")
    print(f"Montante total: R$ {agencia.montante_total():.2f}")


# Cria e vincula uma nova conta (Corrente ou Poupança) a um cliente existente
def cadastrar_conta(banco):
    agencia = obter_agencia(banco)
    numero = input("Numero da conta: ").strip()
    if numero == "":
        print("Número da conta inválido.")
        return
    if banco.procurar_conta(numero) is not None:
        print("Este numero de conta ja esta no sistema!")
        return
    cpf = limpar_cpf(input("CPF do titular: "))
    cliente = obter_cliente(banco, cpf)
    print("\nTipos de conta disponíveis:")
    print("1 - Corrente")
    print("2 - Poupança")
    tipo = TIPOS_CONTA.get(input("Escolha o tipo da conta (1/2): ").strip())
    if tipo is None:
        print("Tipo de conta inválido.")
        return
    conta = ContaFactory.criar(tipo, numero, cliente=cliente, agencia=agencia)
    banco.cadastrar_conta(conta)
    print(f"Conta {NOMES_TIPO[tipo]} cadastrada com sucesso!")


# Lista todas as contas cadastradas no banco
def listar_contas(banco):
    if not banco.contas:
        print("\nNenhuma conta cadastrada.")
        return
    print("\n--- CONTAS ---")
    for conta in banco.contas:
        exibir_conta(conta)


# Busca e exibe uma conta específica pelo número
def procurar_conta(banco):
    conta = obter_conta(banco, input("Numero da conta: ").strip())
    exibir_conta(conta)


# Lista todas as contas pertencentes a um determinado CPF
def procurar_contas_por_cpf(banco):
    cpf = limpar_cpf(input("CPF do titular: "))
    cliente = obter_cliente(banco, cpf)
    contas = cliente.listar_contas()
    if not contas:
        print("\nNenhuma conta encontrada para este CPF.")
        return
    for conta in contas:
        exibir_conta(conta)


# Exibe o saldo atual e o saldo disponível (considerando limite) de uma conta
def consultar_saldo(banco):
    conta = obter_conta(banco, input("Numero da conta: ").strip())
    print(f"\nSaldo: R$ {conta.consultar_saldo():.2f}")
    print(f"Disponível para uso: R$ {conta.saldo_disponivel():.2f}")


# Realiza um depósito na conta informada
def depositar(banco):
    conta = obter_conta(banco, input("Numero da conta: ").strip())
    conta.depositar(ler_valor("Valor do deposito: "))
    print(f"Depósito realizado. Saldo atual: R$ {conta.saldo:.2f}")


# Realiza um saque na conta informada
def sacar(banco):
    conta = obter_conta(banco, input("Numero da conta: ").strip())
    conta.sacar(ler_valor("Valor do saque: "))
    print(f"Saque realizado. Saldo atual: R$ {conta.saldo:.2f}")


# Realiza uma transferência entre duas contas
def transferir(banco):
    origem = obter_conta(banco, input("Numero da conta de origem: ").strip())
    destino = obter_conta(banco, input("Numero da conta destino: ").strip())
    origem.transferir(destino, ler_valor("Valor da transferencia: "))
    print(f"Transferência realizada. Saldo atual da origem: R$ {origem.saldo:.2f}")


# Exibe o montante financeiro total do banco
def montante_total(banco):
    total = obter_agencia(banco).montante_total()
    print("\n--- RELATORIO DO BANCO ---")
    print(f"\nO montante total do banco é: R$ {total:.2f}\n")


# Filtra e exibe apenas as contas com saldo positivo
def contas_saldo_positivo(banco):
    positivas = list(filter(lambda conta: conta.saldo > 0, banco.contas))
    print("\n--- CONTAS COM SALDO POSITIVO ---")
    if not positivas:
        print("Nenhuma conta com saldo positivo.")
    for conta in positivas:
        exibir_conta(conta)
    print()


# Exibe a conta com o maior saldo do banco
def conta_maior_saldo(banco):
    conta = max(banco.contas, key=lambda c: c.saldo, default=None)
    if conta is None:
        print("\nNenhuma conta cadastrada.\n")
        return
    print(f"\nMaior saldo: conta {conta.numero} com R$ {conta.saldo:.2f}\n")


# Exibe a conta com o menor saldo do banco
def conta_menor_saldo(banco):
    conta = min(banco.contas, key=lambda c: c.saldo, default=None)
    if conta is None:
        print("\nNenhuma conta cadastrada.\n")
        return
    print(f"\nMenor saldo: conta {conta.numero} com R$ {conta.saldo:.2f}\n")


# Exibe o painel geral (Dashboard) com os indicadores consolidados do banco
def mostrar_dashboard(banco):
    dados = banco.montar_dashboard()
    maior_conta = dados.maior_saldo_conta or "-"
    menor_conta = dados.menor_saldo_conta or "-"
    print("\n===== DASHBOARD LMS BANK =====")
    print(f"Número de clientes: {dados.num_clientes}")
    print(f"Número de agências: {dados.num_agencias}")
    print(f"Número de contas:   {dados.num_contas}")
    print(f"Saldo total:        R$ {dados.saldo_total:.2f}")
    print(f"Saldo médio:        R$ {dados.saldo_medio:.2f}")
    print(f"Maior saldo:        R$ {dados.maior_saldo:.2f} (conta {maior_conta})")
    print(f"Menor saldo:        R$ {dados.menor_saldo:.2f} (conta {menor_conta})")
    print("==============================\n")


# Dicionário que associa cada opção do menu à sua respectiva função
ACOES = {
    "1": cadastrar_cliente,
    "2": listar_clientes,
    "3": procurar_cliente,
    "4": ver_agencia,
    "5": cadastrar_conta,
    "6": listar_contas,
    "7": procurar_conta,
    "8": procurar_contas_por_cpf,
    "9": consultar_saldo,
    "10": depositar,
    "11": sacar,
    "12": transferir,
    "13": montante_total,
    "14": contas_saldo_positivo,
    "15": conta_maior_saldo,
    "16": conta_menor_saldo,
    "17": mostrar_dashboard,
}


# Função principal que controla o ciclo de vida do banco e o loop do menu
def main():
    banco = Banco.get_instancia()
    banco.iniciar()
    try:
        while True:
            menu()
            opcao = input("Escolha uma opcao: ").strip()
            if opcao == "0":
                print("\nObrigado. Volte sempre! | LMS Bank.")
                break
            acao = ACOES.get(opcao)
            if acao is None:
                print("\nOpção inválida! Tente novamente.")
                continue
            try:
                acao(banco)
            except BancoError as erro:
                print(f"\n{erro}")
    finally:
        banco.encerrar()


# Executa a aplicação apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    main()
