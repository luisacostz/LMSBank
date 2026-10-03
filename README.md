# LMSBank

Sistema bancário desenvolvido em Python para fins acadêmicos. O projeto aplica conceitos de modularização e simula as operações fundamentais de uma instituição financeira. 

**Autores:** Luísa Costa, Murilo Santana e Sarah Beatriz


## Estruturas de dados

Todos os dados são **dicionários** e **listas de dicionários**:

* **Cliente:** `{"nome", "cpf", "data_nascimento", "email", "telefone", "endereco"}`
* **Agência:** `{"numero_agencia", "nome", "telefone", "endereco"}`
* **Conta:** `{"numero", "clientes", "agencia", "saldo", "tipo", ...}`, onde `clientes` é a lista de CPFs dos titulares (mais de um CPF = conta conjunta). Cada tipo de conta tem um campo extra: `limite` (corrente), `taxa_rendimento` (poupança) ou `empregador` (salário).

## Persistência

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
* `principal/relatorio.py`: agregação de dados e estatísticas do banco.
* `principal/armazenamento.py`: leitura e gravação do `banco.json`.
* `testes/`: testes automatizados, em pasta separada da estrutura do projeto (`test_cliente.py`, `test_conta.py`, `test_cpf.py` e `test_relatorio.py`). O `conftest.py` configura o caminho dos módulos para o pytest.
* `banco.json`: dados de exemplo.