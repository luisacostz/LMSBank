"""
Módulo: app.py
Descrição: Rotas Flask do LMS Bank. Faz a "cola" entre o banco.json, as funções de principal/ e web/dashboard.py, e as páginas em templates/.
"""

import contextlib
import io
import os
import sys
from flask import Flask, redirect, render_template, request, url_for

# Adiciona o diretório principal/ ao caminho do Python para permitir a importação dos módulos base do sistema.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "principal"))

# Importa as regras de negócio e manipulação de dados definidas no núcleo da aplicação.
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

# Inicializa a aplicação Flask e define a chave secreta (necessária para exibir mensagens flash de erro/sucesso).
app = Flask(__name__)
app.secret_key = "lmsbank-etapa4"

def carregar():
    """Lê o banco.json a cada requisição, garantindo que os dados estejam atualizados."""
    # Define o caminho do diretório raiz e altera o diretório de trabalho temporariamente.
    raiz_projeto = os.path.join(os.path.dirname(__file__), "..")
    diretorio_atual = os.getcwd()
    os.chdir(raiz_projeto)
    
    try:
        return carregar_dados() # Busca as listas de clientes, agências e contas
    finally:
        # Garante o retorno ao diretório original, mesmo que ocorra erro na leitura
        os.chdir(diretorio_atual)

def gravar(clientes, agencias, contas):
    """Sobrescreve o banco.json com as listas atualizadas após qualquer operação de escrita."""
    raiz_projeto = os.path.join(os.path.dirname(__file__), "..")
    diretorio_atual = os.getcwd()
    os.chdir(raiz_projeto)
    
    try:
        salvar_dados(clientes, agencias, contas)
    finally:
        os.chdir(diretorio_atual)

def chamar_e_capturar(funcao, *args, **kwargs):
    """
    Executa uma função do núcleo (que originalmente usaria print no terminal) 
    e captura a saída de texto (stdout) para exibi-la como mensagem no navegador.
    """
    buffer = io.StringIO()
    # Redireciona tudo que a função 'printar' para a variável 'buffer'
    with contextlib.redirect_stdout(buffer):
        retorno = funcao(*args, **kwargs)
    return retorno, buffer.getvalue().strip()

def valor_valido(texto):
    """Valida se uma string inserida no formulário é um número positivo, aceitando vírgula ou ponto."""
    texto = texto.strip().replace(",", ".")
    # Retira o primeiro ponto decimal e verifica se o que sobrou são apenas dígitos
    return texto.replace(".", "", 1).isdigit()

def flash(mensagem, categoria="ok"):
    """Cria um atalho (wrapper) para a função flash do Flask definindo 'ok' como categoria padrão."""
    from flask import flash as flask_flash
    flask_flash(mensagem, categoria)


@app.route("/clientes")
def clientes():
    """Lista todos os clientes ou filtra por um CPF específico via Query String (GET)."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    cpf_buscado = request.args.get("cpf", "").strip()

    if cpf_buscado:
        encontrado = procurar_cliente(clientes_lista, cpf_buscado)
        resultado = [encontrado] if encontrado else []
    else:
        resultado = clientes_lista

    return render_template(
        "clientes.html",
        ativo="clientes", # Variável para marcar o menu ativo no HTML
        clientes=resultado,
        cpf_buscado=cpf_buscado,
    )

@app.route("/clientes/novo", methods=["GET", "POST"])
def cliente_novo():
    """Exibe o formulário de cadastro (GET) e processa os dados enviados (POST)."""
    if request.method == "GET":
        return render_template("cliente_novo.html", ativo="clientes")

    clientes_lista, agencias_lista, contas_lista = carregar()
    cpf = limpar_cpf(request.form.get("cpf", ""))

    # Validação rigorosa de CPF antes do cadastro
    if not validar_cpf(cpf):
        flash("CPF inválido! Precisa ter 11 números e os dígitos verificadores corretos.", "erro")
        return redirect(url_for("cliente_novo"))

    # Verifica duplicidade
    if procurar_cliente(clientes_lista, cpf):
        flash("Este CPF já está cadastrado no sistema!", "erro")
        return redirect(url_for("cliente_novo"))

    # Executa cadastro e salva alterações
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
    """Carrega e exibe a listagem geral das agências cadastradas."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    return render_template("agencias.html", ativo="agencias", agencias=agencias_lista)

@app.route("/agencias/novo", methods=["GET", "POST"])
def agencia_novo():
    """Gere o formulário (GET) e a inserção de uma nova agência no banco de dados (POST)."""
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


# ==========================================
# ROTAS DE CONTAS
# ==========================================

@app.route("/contas")
def contas():
    """Exibe as contas. Permite filtrar apenas por contas com saldo positivo via Query String."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    somente_positivas = request.args.get("saldo") == "positivo"

    resultado = contas_lista
    if somente_positivas:
        resultado = contas_saldo_positivo(contas_lista)

    return render_template(
        "contas.html",
        ativo="contas",
        contas=resultado,
        total_contas=len(contas_lista),
        somente_positivas=somente_positivas,
    )

@app.route("/contas/novo", methods=["GET", "POST"])
def conta_novo():
    """Cria novas contas (Corrente, Poupança, Salário), vinculando-as a clientes e agências existentes."""
    clientes_lista, agencias_lista, contas_lista = carregar()

    if request.method == "GET":
        # Passa as agências para popular o campo de seleção (select) no HTML
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

    # Processa CPFs inseridos, separados por vírgula, e valida se o cliente existe no sistema
    cpfs_vinculados = []
    erros = []
    for pedaco in texto_titulares.split(","):
        cpf_bruto = pedaco.strip()
        if not cpf_bruto:
            continue
        cpf = limpar_cpf(cpf_bruto)
        if not procurar_cliente(clientes_lista, cpf):
            erros.append(f"Cliente com CPF {cpf_bruto} não encontrado.")
        elif cpf not in cpfs_vinculados: # Evita adicionar o mesmo CPF duas vezes
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


# ==========================================
# ROTAS DE OPERAÇÕES BANCÁRIAS
# ==========================================

@app.route("/operacoes")
def operacoes():
    """Painel central onde são feitos depósitos, saques, transferências e verificação de saldo."""
    return render_template("operacoes.html", ativo="operacoes", resultado_saldo={})

@app.route("/operacoes/depositar", methods=["POST"])
def op_depositar():
    """Trata a submissão do formulário de depósito."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()
    texto_valor = request.form.get("valor", "")
    depositante = request.form.get("depositante", "").strip()

    if not valor_valido(texto_valor):
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    valor = float(texto_valor.strip().replace(",", "."))

    # Realiza o depósito e captura o log da operação para mostrar como feedback ao usuário
    _, mensagem = chamar_e_capturar(depositar, contas_lista, numero_conta, valor, depositante)
    gravar(clientes_lista, agencias_lista, contas_lista)
    
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))

@app.route("/operacoes/sacar", methods=["POST"])
def op_sacar():
    """Trata a submissão do formulário de saque, validando valor antes da execução."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()
    texto_valor = request.form.get("valor", "")

    if not valor_valido(texto_valor):
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    valor = float(texto_valor.strip().replace(",", "."))

    _, mensagem = chamar_e_capturar(sacar, contas_lista, numero_conta, valor)
    gravar(clientes_lista, agencias_lista, contas_lista)
    
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))

@app.route("/operacoes/transferir", methods=["POST"])
def op_transferir():
    """Maneja a transferência entre duas contas distintas."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_origem = request.form.get("numero_origem", "").strip()
    numero_destino = request.form.get("numero_destino", "").strip()
    texto_valor = request.form.get("valor", "")

    if not valor_valido(texto_valor):
        flash("Valor inválido. Digite apenas números.", "erro")
        return redirect(url_for("operacoes"))

    valor = float(texto_valor.strip().replace(",", "."))

    _, mensagem = chamar_e_capturar(transferir, contas_lista, numero_origem, numero_destino, valor)
    gravar(clientes_lista, agencias_lista, contas_lista)
    
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))

@app.route("/operacoes/saldo", methods=["POST"])
def op_saldo():
    """Busca o saldo de uma conta específica e injeta a resposta na própria tela de operações."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()

    _, mensagem = chamar_e_capturar(consultar_saldo, contas_lista, numero_conta)
    # Aqui renderizamos o template diretamente (em vez de redirect) para injetar o 'resultado_saldo' no HTML
    return render_template(
        "operacoes.html",
        ativo="operacoes",
        resultado_saldo={"numero": numero_conta, "texto": mensagem or "Conta não encontrada."},
    )

@app.route("/operacoes/rendimento", methods=["POST"])
def op_rendimento():
    """Aplica as taxas de rendimento nas contas poupança."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    numero_conta = request.form.get("numero_conta", "").strip()

    _, mensagem = chamar_e_capturar(aplicar_rendimento, contas_lista, numero_conta)
    gravar(clientes_lista, agencias_lista, contas_lista)
    
    flash(mensagem or "Operação concluída.")
    return redirect(url_for("operacoes"))

@app.route("/dashboard")
def dashboard():
    """Reúne e processa dados estatísticos e analíticos do banco para o painel de visualização (Dashboard)."""
    clientes_lista, agencias_lista, contas_lista = carregar()
    agencia_consultada = request.args.get("agencia", "").strip()

    montante_agencia = 0.0
    # Calcula o montante total de uma agência específica caso ela tenha sido pesquisada via Query String
    if agencia_consultada:
        montante_agencia = montante_por_agencia(contas_lista, agencia_consultada)

    return render_template(
        "dashboard.html",
        ativo="dashboard",
        dados=montar_dashboard(clientes_lista, agencias_lista, contas_lista),
        agencia_destaque=agencia_mais_clientes(contas_lista),
        contas_conjuntas=contar_contas_conjuntas(contas_lista),
        agencia_consultada=agencia_consultada,
        montante_agencia=montante_agencia,
    )

@app.route("/")
def index():
    """Rota raiz da aplicação; redireciona imediatamente o usuário para o dashboard."""
    return redirect(url_for("dashboard"))


# Inicia o servidor Flask com o modo de depuração ativado para desenvolvimento.
if __name__ == "__main__":
    app.run(debug=True)