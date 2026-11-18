# Registra o salvamento final do banco quando o processo da aplicação termina.
import atexit
# Monta caminhos absolutos a partir do arquivo da aplicação.
import os
# Permite incluir a pasta principal no caminho de busca de módulos Python.
import sys

# Importa a aplicação Flask, as mensagens ao usuário, os redirecionamentos, os templates e os dados das requisições.
from flask import Flask, flash, redirect, render_template, request, url_for

RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(RAIZ_PROJETO, "principal"))

# Importa o banco compartilhado pelas rotas web.
from banco import Banco
# Importa a classe usada para criar novos clientes.
from cliente import Cliente
# Importa a fábrica que cria contas bancárias conforme o tipo solicitado.
from conta_factory import ContaFactory
# Importa a função que normaliza o CPF informado nos formulários.
from cpf import limpar_cpf
# Importa as exceções de regra de negócio tratadas pelas rotas.
from excecoes import BancoError, OperacaoInvalidaError, ValorInvalidoError

CAMINHO_JSON = os.path.join(RAIZ_PROJETO, "banco.json")
NOMES_TIPO = {"corrente": "Corrente", "poupanca": "Poupança"}

app = Flask(__name__)
app.secret_key = "lmsbank-etapa5"

banco = Banco.get_instancia()
banco.iniciar(CAMINHO_JSON)
atexit.register(lambda: banco.encerrar(CAMINHO_JSON))


def ler_valor(texto):
    # Converte o valor informado para número e transforma entradas inválidas em erro de domínio.
    try:
        return float(str(texto).strip().replace(",", "."))
    except ValueError:
        raise ValorInvalidoError("Valor inválido. Digite apenas números.")


def obter_conta(numero):
    # Localiza uma conta e informa quando o número não existe no banco.
    conta = banco.procurar_conta(numero)
    if conta is None:
        raise OperacaoInvalidaError("Conta não encontrada.")
    return conta


def obter_cliente(cpf):
    # Localiza um cliente pelo CPF e informa quando ele não está cadastrado.
    cliente = banco.procurar_cliente(cpf)
    if cliente is None:
        raise OperacaoInvalidaError("Cliente não encontrado.")
    return cliente


@app.route("/")
def index():
    # Encaminha a página inicial para o painel de indicadores.
    return redirect(url_for("dashboard"))


@app.route("/clientes")
def clientes():
    # Lista os clientes ou filtra a listagem pelo CPF da consulta.
    cpf_buscado = request.args.get("cpf", "").strip()
    if cpf_buscado:
        encontrado = banco.procurar_cliente(cpf_buscado)
        resultado = [encontrado] if encontrado else []
    else:
        resultado = banco.clientes
    return render_template(
        "clientes.html",
        ativo="clientes",
        clientes=resultado,
        cpf_buscado=cpf_buscado,
    )


@app.route("/clientes/novo", methods=["GET", "POST"])
def cliente_novo():
    # Exibe o formulário de cliente e processa o cadastro enviado.
    if request.method == "GET":
        return render_template("cliente_novo.html", ativo="clientes")
    try:
        cliente = Cliente(
            nome=request.form.get("nome", "").strip(),
            cpf=request.form.get("cpf", ""),
            data_nascimento=request.form.get("data_nascimento", "").strip(),
            email=request.form.get("email", "").strip(),
            telefone=request.form.get("telefone", "").strip(),
            endereco=request.form.get("endereco", "").strip(),
        )
        banco.cadastrar_cliente(cliente)
    except BancoError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("cliente_novo"))
    flash("Cliente cadastrado com sucesso!", "ok")
    return redirect(url_for("clientes"))


@app.route("/contas")
def contas():
    # Lista as contas e, quando solicitado, mostra apenas as de saldo positivo.
    somente_positivas = request.args.get("saldo") == "positivo"
    resultado = banco.contas
    if somente_positivas:
        resultado = list(filter(lambda conta: conta.saldo > 0, banco.contas))
    return render_template(
        "contas.html",
        ativo="contas",
        contas=resultado,
        total_contas=len(banco.contas),
        somente_positivas=somente_positivas,
    )


@app.route("/contas/novo", methods=["GET", "POST"])
def conta_novo():
    # Exibe o formulário de conta e cria uma conta vinculada ao cliente e à agência.
    if request.method == "GET":
        return render_template("conta_novo.html", ativo="contas", agencia=banco.agencia)
    try:
        if banco.agencia is None:
            raise OperacaoInvalidaError("O banco não tem agência cadastrada.")
        numero = request.form.get("numero", "").strip()
        if numero == "":
            raise OperacaoInvalidaError("Número da conta inválido.")
        cliente = obter_cliente(limpar_cpf(request.form.get("cpf", "")))
        tipo = request.form.get("tipo", "corrente")
        conta = ContaFactory.criar(tipo, numero, cliente=cliente, agencia=banco.agencia)
        banco.cadastrar_conta(conta)
    except BancoError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("conta_novo"))
    flash(f"Conta {NOMES_TIPO[conta.tipo()]} cadastrada com sucesso!", "ok")
    return redirect(url_for("contas"))


@app.route("/operacoes")
def operacoes():
    # Exibe a página que reúne as operações bancárias disponíveis.
    return render_template("operacoes.html", ativo="operacoes", resultado_saldo={})


@app.route("/operacoes/depositar", methods=["POST"])
def op_depositar():
    # Processa o depósito informado e mostra o resultado da operação.
    try:
        conta = obter_conta(request.form.get("numero_conta", ""))
        conta.depositar(ler_valor(request.form.get("valor", "")))
    except BancoError as erro:
        flash(str(erro), "erro")
    else:
        flash(f"Depósito realizado. Saldo atual: R$ {conta.saldo:.2f}", "ok")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/sacar", methods=["POST"])
def op_sacar():
    # Processa o saque informado e mostra o resultado da operação.
    try:
        conta = obter_conta(request.form.get("numero_conta", ""))
        conta.sacar(ler_valor(request.form.get("valor", "")))
    except BancoError as erro:
        flash(str(erro), "erro")
    else:
        flash(f"Saque realizado. Saldo atual: R$ {conta.saldo:.2f}", "ok")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/transferir", methods=["POST"])
def op_transferir():
    # Transfere o valor informado entre as contas de origem e destino.
    try:
        origem = obter_conta(request.form.get("numero_origem", ""))
        destino = obter_conta(request.form.get("numero_destino", ""))
        origem.transferir(destino, ler_valor(request.form.get("valor", "")))
    except BancoError as erro:
        flash(str(erro), "erro")
    else:
        flash(f"Transferência realizada. Saldo atual da origem: R$ {origem.saldo:.2f}", "ok")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/saldo", methods=["POST"])
def op_saldo():
    # Consulta o saldo e o valor disponível de uma conta.
    numero = request.form.get("numero_conta", "").strip()
    try:
        conta = obter_conta(numero)
    except BancoError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("operacoes"))
    texto = (
        f"Saldo: R$ {conta.consultar_saldo():.2f}\n"
        f"Disponível para uso: R$ {conta.saldo_disponivel():.2f}"
    )
    return render_template(
        "operacoes.html",
        ativo="operacoes",
        resultado_saldo={"numero": conta.numero, "texto": texto},
    )


@app.route("/dashboard")
def dashboard():
    # Monta e apresenta os indicadores atuais do banco.
    return render_template(
        "dashboard.html",
        ativo="dashboard",
        dados=banco.montar_dashboard(),
        agencia=banco.agencia,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
