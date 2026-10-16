"""
Módulo: app.py
Descrição: Rotas Flask do LMS Bank. Faz a "cola" entre o banco.json, as
funções de principal/ e web/dashboard.py, e as páginas em templates/.
"""

import contextlib
import io
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "principal"))

from flask import Flask, redirect, render_template, request, url_for

from armazenamento import carregar_dados, salvar_dados
from cliente import cadastrar_cliente, procurar_cliente
from agencia import cadastrar_agencia, procurar_agencia
from conta import (
    cadastrar_conta,
    procurar_conta,
    consultar_saldo,
    depositar,
    sacar,
    transferir,
    aplicar_rendimento,
)
from cpf import limpar_cpf, validar_cpf
from relatorio import montante_por_agencia, agencia_mais_clientes, contar_contas_conjuntas
from dashboard import contas_saldo_positivo, montar_dashboard

app = Flask(__name__)
# Necessária para as mensagens flash (guardadas na sessão). Projeto acadêmico, chave fixa.
app.secret_key = "lmsbank-etapa4"

def carregar():
    """Lê o banco.json a cada requisição."""
    raiz_projeto = os.path.join(os.path.dirname(__file__), "..")
    diretorio_atual = os.getcwd()
    os.chdir(raiz_projeto)
    try:
        return carregar_dados()
    finally:
        os.chdir(diretorio_atual)


def gravar(clientes, agencias, contas):
    raiz_projeto = os.path.join(os.path.dirname(__file__), "..")
    diretorio_atual = os.getcwd()
    os.chdir(raiz_projeto)
    try:
        salvar_dados(clientes, agencias, contas)
    finally:
        os.chdir(diretorio_atual)


def chamar_e_capturar(funcao, *args, **kwargs):
    """Executa uma função de principal/ capturando o que ela imprime, pra reaproveitar a mesma mensagem no navegador."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        retorno = funcao(*args, **kwargs)
    return retorno, buffer.getvalue().strip()


def valor_para_float(texto):
    """Aceita vírgula ou ponto decimal. Devolve None se inválido."""
    texto = texto.strip().replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def flash(mensagem, categoria="ok"):
    from flask import flash as flask_flash
    flask_flash(mensagem, categoria)


@app.route("/clientes")
def clientes():
    clientes_lista, agencias_lista, contas_lista = carregar()
    cpf_buscado = request.args.get("cpf", "").strip()

    if cpf_buscado:
        encontrado = procurar_cliente(clientes_lista, cpf_buscado)
        resultado = [encontrado] if encontrado else []
    else:
        resultado = clientes_lista

    return render_template(
        "clientes.html",
        ativo="clientes",
        clientes=resultado,
        cpf_buscado=cpf_buscado,
    )


@app.route("/clientes/novo", methods=["GET", "POST"])
def cliente_novo():
    if request.method == "GET":
        return render_template("cliente_novo.html", ativo="clientes")

    clientes_lista, agencias_lista, contas_lista = carregar()
    cpf = limpar_cpf(request.form.get("cpf", ""))

    if not validar_cpf(cpf):
        flash("CPF inválido! Precisa ter 11 números e os dígitos verificadores corretos.", "erro")
        return redirect(url_for("cliente_novo"))

    if procurar_cliente(clientes_lista, cpf):
        flash("Este CPF já está cadastrado no sistema!", "erro")
        return redirect(url_for("cliente_novo"))

    cadastrar_cliente(
        clientes_lista,
        request.form.get("nome", "").strip(),
        cpf,
        request.form.get("data_nascimento", "").strip(),
        request.form.get("email", "").strip(),
        request.form.get("telefone", "").strip(),
        request.form.get("endereco", "").strip(),
    )
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash("Cliente cadastrado com sucesso!")
    return redirect(url_for("clientes"))



@app.route("/agencias")
def agencias():
    clientes_lista, agencias_lista, contas_lista = carregar()
    return render_template("agencias.html", ativo="agencias", agencias=agencias_lista)


@app.route("/agencias/novo", methods=["GET", "POST"])
def agencia_novo():
    if request.method == "GET":
        return render_template("agencia_novo.html", ativo="agencias")

    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_agencia = request.form.get("numero_agencia", "").strip()

    if procurar_agencia(agencias_lista, numero_agencia):
        flash("Esta agência já está no sistema!", "erro")
        return redirect(url_for("agencia_novo"))

    cadastrar_agencia(
        agencias_lista,
        numero_agencia,
        request.form.get("nome", "").strip(),
        request.form.get("telefone", "").strip(),
        request.form.get("endereco", "").strip(),
    )
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash("Agência cadastrada com sucesso!")
    return redirect(url_for("agencias"))


@app.route("/contas")
def contas():
    clientes_lista, agencias_lista, contas_lista = carregar()
    somente_positivas = request.args.get("saldo") == "positivo"

    resultado = contas_lista
    if somente_positivas:
        filtradas = contas_saldo_positivo(contas_lista)
        if filtradas is None:
            # dashboard.py ainda não implementou o filtro: mostra tudo e avisa
            flash("Filtro de saldo positivo ainda não implementado (dashboard.py).", "erro")
            somente_positivas = False
        else:
            resultado = filtradas

    return render_template(
        "contas.html",
        ativo="contas",
        contas=resultado,
        total_contas=len(contas_lista),
        somente_positivas=somente_positivas,
    )


@app.route("/contas/novo", methods=["GET", "POST"])
def conta_novo():
    clientes_lista, agencias_lista, contas_lista = carregar()

    if request.method == "GET":
        return render_template("conta_novo.html", ativo="contas", agencias=agencias_lista)

    numero = request.form.get("numero", "").strip()
    if procurar_conta(contas_lista, numero):
        flash("Este número de conta já está no sistema!", "erro")
        return redirect(url_for("conta_novo"))

    numero_agencia = request.form.get("numero_agencia", "").strip()
    if not procurar_agencia(agencias_lista, numero_agencia):
        flash("Agência não encontrada. Cadastre a agência antes.", "erro")
        return redirect(url_for("conta_novo"))

    tipo = request.form.get("tipo", "corrente").strip().lower()
    empregador = request.form.get("empregador", "").strip()
    texto_titulares = request.form.get("titulares", "")

    cpfs_vinculados = []
    erros = []
    for pedaco in texto_titulares.split(","):
        cpf_bruto = pedaco.strip()
        if not cpf_bruto:
            continue
        cpf = limpar_cpf(cpf_bruto)
        if not procurar_cliente(clientes_lista, cpf):
            erros.append(f"Cliente com CPF {cpf_bruto} não encontrado.")
        elif cpf not in cpfs_vinculados:
            cpfs_vinculados.append(cpf)

    if erros:
        flash(" ".join(erros), "erro")
        return redirect(url_for("conta_novo"))

    if not cpfs_vinculados:
        flash("Informe ao menos um titular válido.", "erro")
        return redirect(url_for("conta_novo"))

    cadastrar_conta(contas_lista, numero, cpfs_vinculados, numero_agencia, tipo, empregador)
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash(f"Conta {tipo.capitalize()} cadastrada com sucesso!")
    return redirect(url_for("contas"))


@app.route("/operacoes")
def operacoes():
    return render_template("operacoes.html", ativo="operacoes", resultado_saldo=None)


@app.route("/operacoes/depositar", methods=["POST"])
def op_depositar():
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()
    valor = valor_para_float(request.form.get("valor", ""))
    depositante = request.form.get("depositante", "").strip()

    if valor is None:
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    _, mensagem = chamar_e_capturar(depositar, contas_lista, numero_conta, valor, depositante)
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/sacar", methods=["POST"])
def op_sacar():
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()
    valor = valor_para_float(request.form.get("valor", ""))

    if valor is None:
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    _, mensagem = chamar_e_capturar(sacar, contas_lista, numero_conta, valor)
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/transferir", methods=["POST"])
def op_transferir():
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_origem = request.form.get("numero_origem", "").strip()
    numero_destino = request.form.get("numero_destino", "").strip()
    valor = valor_para_float(request.form.get("valor", ""))

    if valor is None:
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    _, mensagem = chamar_e_capturar(transferir, contas_lista, numero_origem, numero_destino, valor)
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))


@app.route("/operacoes/saldo", methods=["POST"])
def op_saldo():
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()

    _, mensagem = chamar_e_capturar(consultar_saldo, contas_lista, numero_conta)
    return render_template(
        "operacoes.html",
        ativo="operacoes",
        resultado_saldo={"numero": numero_conta, "texto": mensagem or "Conta não encontrada."},
    )


@app.route("/operacoes/rendimento", methods=["POST"])
def op_rendimento():
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()

    _, mensagem = chamar_e_capturar(aplicar_rendimento, contas_lista, numero_conta)
    gravar(clientes_lista, agencias_lista, contas_lista)
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))


@app.route("/dashboard")
def dashboard():
    clientes_lista, agencias_lista, contas_lista = carregar()
    agencia_consultada = request.args.get("agencia", "").strip()

    montante_agencia = None
    if agencia_consultada:
        montante_agencia = montante_por_agencia(contas_lista, agencia_consultada)

    return render_template(
        "dashboard.html",
        ativo="dashboard",
        dados=montar_dashboard(clientes_lista, agencias_lista, contas_lista),
        agencia_destaque=agencia_mais_clientes(contas_lista) or None,
        contas_conjuntas=contar_contas_conjuntas(contas_lista),
        agencia_consultada=agencia_consultada or None,
        montante_agencia=montante_agencia,
    )


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
