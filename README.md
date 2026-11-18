# LMSBank

Sistema bancário desenvolvido em Python para fins acadêmicos, com interface de console e interface web (Flask). Na Etapa 5 o projeto deixou de usar dicionários e passou a ser orientado a objetos, com padrões de projeto.

**Autores:** Luísa Costa, Murilo Santana e Sarah Beatriz.

## Modelo de classes

O diagrama completo está em `docs/modelo_classes.puml` (PlantUML).

| Classe | Papel |
|--------|-------|
| `Banco` | Singleton. Guarda a agência, os clientes e as contas, e controla a leitura e a gravação do JSON. |
| `Agencia` | Única agência do banco. Conhece as suas contas e calcula o montante total. |
| `Cliente` | Dados do cliente (CPF validado na criação). Um cliente tem várias contas. |
| `Conta` (abstrata) | Regras comuns: depositar, sacar, transferir e consultar saldo. |
| `ContaCorrente` | Tem cheque especial (`limite`, padrão R$ 500,00). |
| `ContaPoupanca` | Rende todo mês (`taxa_rendimento`, padrão 0,5% ao mês) e guarda a data do `ultimo_rendimento`. |
| `ContaFactory` | Fábrica que cria a conta certa a partir do tipo. |
| `Dashboard` | Guarda os números do painel (contagens, saldo total, médio, maior e menor). |
| `BancoError` e filhas | Exceções do banco: `ValorInvalidoError`, `SaldoInsuficienteError`, `OperacaoInvalidaError`, `TipoContaInvalidoError` e `CpfInvalidoError`. |

Cada conta pertence a **um** cliente e à **única** agência do banco.

## Padrões de projeto

### Singleton (`Banco`)
Só existe um `Banco` no programa. `Banco.get_instancia()` cria o objeto na primeira chamada e devolve sempre o mesmo nas seguintes. Assim, o console e o Flask trabalham com os mesmos dados em memória, sem passar listas de um lado para o outro.

### Factory Method (`ContaFactory`)
Quem precisa de uma conta chama `ContaFactory.criar("corrente" | "poupanca", ...)` ou `ContaFactory.from_dict(...)` e não precisa conhecer as classes concretas. Para criar um novo tipo de conta, basta incluí-lo no dicionário `_TIPOS` da fábrica. Tipo desconhecido lança `TipoContaInvalidoError`.

### Template Method (`Conta`)
`Conta.sacar()` define os passos (validar o valor, conferir o saldo disponível e debitar) e chama `saldo_disponivel()`, que cada subclasse implementa. A corrente soma o cheque especial e a poupança usa só o saldo.

## Persistência

Os dados ficam em `banco.json`, com este formato:
```json
{
    "agencia": {"numero_agencia": "0001", "nome": "Sede", "telefone": "1111-2222", "endereco": "..."},
    "clientes": [{"nome": "...", "cpf": "52998224725", "data_nascimento": "...", "email": "...", "telefone": "...", "endereco": "..."}],
    "contas": [
        {"numero": "1", "cliente_cpf": "52998224725", "saldo": 100.0, "tipo": "corrente", "limite": 500.0},
        {"numero": "2", "cliente_cpf": "52998224725", "saldo": 200.0, "tipo": "poupanca", "taxa_rendimento": 0.005, "ultimo_rendimento": "2026-10-17"}
    ]
}
```
O JSON só é tocado em dois momentos:
* **`Banco.iniciar()`** lê o arquivo, cria `Agencia` e `Cliente` com `from_dict`, cria cada conta pela `ContaFactory` ligando-a ao cliente (pelo `cliente_cpf`) e à agência, e chama `aplicar_rendimento()` das poupanças.
* **`Banco.encerrar()`** monta o dicionário com `to_dict` de cada objeto e grava o arquivo.

No console, `encerrar()` roda ao sair do programa. No Flask, roda no encerramento do servidor, por meio do `atexit`. Por isso o servidor é iniciado com `use_reloader=False`: o reloader criaria um segundo processo com outro `Banco`.

## Rendimento da poupança

A poupança rende a cada mês completo. A conta guarda `ultimo_rendimento` e, ao iniciar o banco, paga os meses completos que passaram desde essa data (juros compostos). Os dias que sobram contam para o próximo rendimento.

## Funcionalidades

* **Clientes:** cadastrar, listar e procurar por CPF.
* **Agência:** ver os dados e o montante total.
* **Contas:** cadastrar (com um único titular), listar, procurar por número e procurar por CPF.
* **Operações:** consultar saldo, depositar, sacar e transferir.
* **Relatórios:** montante total, contas com saldo positivo, conta com maior e menor saldo e dashboard.

Erros de regra de negócio são exceções (`BancoError`). O console imprime a mensagem e o Flask a mostra com `flash`.

## Validação de CPF

Todo CPF é limpo (aceita pontos, traço e espaços) e validado ao criar o `Cliente`: precisa ter 11 números, não pode ter todos os dígitos iguais e os 2 dígitos verificadores precisam estar corretos. O CPF é guardado somente com números.

CPFs válidos para testar: `529.982.247-25`, `111.444.777-35` e `390.533.447-05`.

## Tipos de conta
| Tipo | Regra |
|------|-------|
| Corrente | Possui cheque especial de R$ 500,00, que pode ser usado em saques e transferências. |
| Poupança | Rende 0,5% ao mês, aplicado automaticamente ao iniciar o banco. |

## Estrutura do projeto
* `principal/banco.py`: classe `Banco` (Singleton).
* `principal/cliente.py`, `principal/agencia.py`: entidades, com `to_dict` e `from_dict`.
* `principal/conta.py`, `principal/conta_corrente.py`, `principal/conta_poupanca.py`: hierarquia de contas.
* `principal/conta_factory.py`: fábrica de contas.
* `principal/dashboard.py`: números do painel.
* `principal/excecoes.py`: exceções do banco.
* `principal/armazenamento.py`: leitura e gravação do `banco.json`.
* `principal/cpf.py`: limpeza e validação de CPF.
* `principal/main.py` e `principal/menu.py`: interface de console.
* `testes/`: testes automatizados, uma pasta separada do código.
* `conftest.py` (na raiz): configura o caminho das pastas e zera o `Banco` entre os testes.
* `docs/modelo_classes.puml`: diagrama de classes.
* `banco.json`: dados de exemplo.

## Web
O banco tem uma interface web (Flask + HTML + CSS) que usa o mesmo `Banco`:
* `web/app.py`: rotas Flask. O `Banco` é carregado uma vez, quando o servidor sobe.
* `web/templates/`: páginas HTML (Jinja2). `base.html` é o layout comum.
* `web/static/css/style.css`: estilo visual.

| Página | Rota | O que mostra |
|--------|------|--------------|
| Clientes | `/clientes` | Lista de clientes, busca por CPF e cadastro |
| Contas | `/contas` | Lista de contas; `?saldo=positivo` filtra contas com saldo > 0 |
| Operações | `/operacoes` | Depositar, sacar, transferir e consultar saldo |
| Relatório | `/dashboard` | Nº de clientes, agência e contas, saldo total, saldo médio, maior e menor saldo |

## Como rodar

Console (na raiz do projeto):
```
python principal/main.py
```

Web:
```
cd web
pip install -r requirements.txt
python app.py
```
Depois abrir http://127.0.0.1:5000. Para os dados serem salvos, encerre o servidor com Ctrl+C.

## Como rodar os testes

Na raiz do projeto (a pasta que contém `conftest.py`):
```
pip install pytest
python -m pytest
```

## Créditos e referências

### Validação de CPF (`principal/cpf.py`)
O algoritmo dos dígitos verificadores (pesos de 10 a 2 no 1º dígito e de 11 a 2 no 2º, resto da divisão por 11 menor que 2 vira 0, e recusa de CPFs com todos os dígitos iguais) segue o método explicado nestas fontes. O código foi escrito por nós, com base nessa lógica:
* DIO – *Como criar um validador de CPF com Python*: https://www.dio.me/articles/16-como-criar-um-validador-de-cpf-com-python-8ea27e2db9d0
* Valor Final – *Dígito verificador do CPF: como calcular e validar*: https://valorfinal.com.br/guia/digito-verificador-do-cpf
* TabNews – *Como funciona um gerador de CPF (apenas o conceito)*: https://www.tabnews.com.br/cacatua/como-funciona-um-gerador-de-cpf-apenas-o-conceito

### Padrões de projeto
* Refactoring Guru – Singleton: https://refactoring.guru/pt-br/design-patterns/singleton
* Refactoring Guru – Factory Method: https://refactoring.guru/pt-br/design-patterns/factory-method
* Refactoring Guru – Template Method: https://refactoring.guru/pt-br/design-patterns/template-method

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
