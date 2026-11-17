# LMSBank

Sistema bancário desenvolvido em Python para fins acadêmicos. O projeto aplica conceitos de modularização e simula as operações fundamentais de uma instituição financeira. 

**Autores:** Luísa Costa, Murilo Santana e Sarah Beatriz.

Todos os dados são **dicionários** e **listas de dicionários**:
* **Cliente:** `{"nome", "cpf", "data_nascimento", "email", "telefone", "endereco"}`
* **Agência:** `{"numero_agencia", "nome", "telefone", "endereco"}`
* **Conta:** `{"numero", "clientes", "agencia", "saldo", "tipo", ...}`, onde `clientes` é a lista de CPFs dos titulares (mais de um CPF = conta conjunta). Cada tipo de conta tem um campo extra: `limite` (corrente), `taxa_rendimento` (poupança) ou `empregador` (salário).

Os dados são salvos em `banco.json`, que é um **dicionário** com três listas de dicionários:
```json
{
    "clientes": [],
    "agencias": [],
    "contas": []
}
```
O arquivo é carregado ao iniciar o programa e salvo a cada operação que altera dados.

## Funcionalidades

* **Clientes:** cadastrar, listar e procurar por CPF.
* **Agências:** cadastrar, listar e procurar por número.
* **Contas:** cadastrar (individual ou conjunta), listar, procurar por número da conta e procurar por CPF do titular.
* **Operações:** consultar saldo, depositar, sacar e transferir.
* **Relatórios:** montante total do banco, montante por agência, agência com mais clientes e quantidade de contas conjuntas.
* **Análise financeira (opções 21 a 24 do menu):** contas com saldo positivo, conta com maior saldo, conta com menor saldo e dashboard (nº de clientes, agências e contas, saldo total, saldo médio, maior e menor saldo).

## Validação de CPF

Todo CPF digitado é limpo (aceita pontos, traço e espaços) e validado antes do cadastro: precisa ter 11 números, não pode ter todos os dígitos iguais e os 2 dígitos verificadores precisam estar corretos. O CPF é guardado somente com números.

CPFs válidos para testar: `529.982.247-25`, `111.444.777-35` e `390.533.447-05`.

## Tipos de conta
| Tipo | Regra |
|------|-------|
| Corrente | Possui cheque especial de R$ 500,00, que pode ser usado em saques e transferências. |
| Poupança | Rende 1% sobre o saldo quando o rendimento é aplicado (opção 20 do menu). |
| Salário | Só aceita depósito do empregador cadastrado e não realiza transferências. |

## Estrutura do projeto
* `principal/main.py`: arquivo principal, que carrega os dados e controla o menu.
* `principal/menu.py`: exibe as opções do menu no console.
* `principal/cliente.py`, `principal/conta.py` e `principal/agencia.py`: lógica de cada entidade.
* `principal/cpf.py`: limpeza e validação de CPF.
* `principal/relatorio.py`: agregação de dados e estatísticas do banco. Usa funções de alta ordem (`reduce` para o saldo total, `filter` para contas com saldo positivo, `max` e `min` com `key` para maior e menor saldo) e compreensão de listas (saldos, números das contas positivas, montante por agência, contas conjuntas e linhas de exibição).
* `principal/armazenamento.py`: leitura e gravação do `banco.json`.
* `testes/`: testes automatizados, em pasta separada da estrutura do projeto (`test_cliente.py`, `test_conta.py`, `test_cpf.py`, `test_relatorio.py` e `test_dashboard.py`).
* `conftest.py` (na raiz): configura o caminho das pastas `principal` e `web` para o pytest encontrar os módulos.
* `banco.json`: dados de exemplo.

## Web
Além do console, o banco tem uma interface web (Flask + HTML + CSS) que lê e grava o mesmo `banco.json`:
* `web/app.py`: rotas Flask (clientes, agências, contas, operações, relatório).
* `web/templates/`: páginas HTML (Jinja2). `base.html` é o layout comum.
* `web/static/css/style.css`: estilo visual.
* `web/dashboard.py`: lógica pura do dashboard: reúne os números do relatório na função `montar_dashboard` (saldo total, maior e menor saldo, saldo médio e contagens). Em um banco sem contas os saldos valem `0.00`.

| Página | Rota | O que mostra |
|--------|------|--------------|
| Clientes | `/clientes` | Lista de clientes, busca por CPF e cadastro |
| Agências | `/agencias` | Lista de agências e cadastro |
| Contas | `/contas` | Lista de contas; `?saldo=positivo` filtra contas com saldo > 0 |
| Operações | `/operacoes` | Depositar, sacar, transferir, consultar saldo e rendimento |
| Relatório | `/dashboard` | Nº de clientes, agências e contas, saldo total, saldo médio, maior e menor saldo |

Como rodar
cd web
pip install -r requirements.txt
python app.py

Depois abrir http://127.0.0.1:5000.

Como rodar os testes

Na raiz do projeto (a pasta que contém conftest.py):

pip install pytest
python -m pytest



## Créditos e referências

### Validação de CPF (`principal/cpf.py`)
O algoritmo dos dígitos verificadores (pesos de 10 a 2 no 1º dígito e de 11 a 2 no 2º, resto da divisão por 11 menor que 2 vira 0, e recusa de CPFs com todos os dígitos iguais) segue o método explicado nestas fontes. O código foi escrito por nós, com base nessa lógica:
* DIO – *Como criar um validador de CPF com Python* (usa o mesmo CPF de exemplo `529.982.247-xx` que aparece neste README): https://www.dio.me/articles/16-como-criar-um-validador-de-cpf-com-python-8ea27e2db9d0
* Valor Final – *Dígito verificador do CPF: como calcular e validar*: https://valorfinal.com.br/guia/digito-verificador-do-cpf
* TabNews – *Como funciona um gerador de CPF (apenas o conceito)*: https://www.tabnews.com.br/cacatua/como-funciona-um-gerador-de-cpf-apenas-o-conceito

### Flask (`web/app.py`)
Rotas, `render_template`, `request`, `redirect`/`url_for`, arquivos estáticos e mensagens `flash`:
* Documentação oficial do Flask – Quickstart: https://flask.palletsprojects.com/en/stable/quickstart/
* Siddhartha Roy (DEV Community) – *A complete beginner friendly Python Flask tutorial*: https://dev.to/sid86dev/a-complete-beginner-friendly-python-flask-tutorial-learn-from-basic-template-rendering-to-deploying-in-web-servers-5ack
* Projeto de apoio indicado pelo professor: https://github.com/AnotherOne07/sistema-bancario-progA

### HTML (`web/templates/`)
* MDN Web Docs – Aprender HTML: https://developer.mozilla.org/pt-BR/docs/Learn/HTML
* web.dev – Aprenda HTML: https://web.dev/learn/html/welcome?hl=pt-BR

### CSS (`web/static/css/style.css`)
* MDN Web Docs – Primeiros passos com CSS: https://developer.mozilla.org/pt-BR/docs/Learn/CSS/First_steps
* web.dev – Aprenda CSS: https://web.dev/learn/css?hl=pt-br