# LMSBank

Sistema bancário desenvolvido em Python para fins acadêmicos. O projeto aplica conceitos de modularização e simula as operações fundamentais de uma instituição financeira.

## Funcionalidades

* **Gestão de Entidades:** Registo e manutenção de dados através dos módulos `cliente.py` e `agencia.py`.
* **Operações de Conta:** Listagem, procura, consulta de saldo, depósitos e transferências implementadas no módulo `conta.py`.
* **Relatórios e Estatísticas:** Novo módulo `relatorio.py` para visualizar o montante global do banco, montante por agência, identificar a agência com mais clientes e o número de contas conjuntas.
* **Persistência de Dados:** Carregamento e gravação de ficheiros garantidos pelo módulo `armazenamento.py`.

## Estrutura do Projeto

* `main.py`: Ficheiro principal que inicializa o sistema.
* `menu.py`: Contém a interface interativa de texto com o utilizador.
* `cliente.py` / `conta.py` / `agencia.py`: Lógica de negócio isolada por entidade.
* `relatorio.py`: Lógica dedicada à agregação de dados e estatísticas globais.
* `armazenamento.py`: Manipulação de ficheiros.
* `testes/`: Diretório que contém os ficheiros de testes (ex: `teste_saque`).