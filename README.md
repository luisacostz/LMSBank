# LMSBank

Sistema bancário desenvolvido em Python para fins acadêmicos. O projeto aplica conceitos de modularização, estruturas de repetição e manipulação de listas e tuplas.

## Funcionalidades

* **Gerenciamento de Clientes:** Cadastro, listagem e busca por CPF.
* **Gerenciamento de Agências:** Criação, listagem e busca de agências.
* **Gerenciamento de Contas:** Abertura de contas vinculadas a clientes e agências específicas.
* **Operações Financeiras:** Consulta de saldo, realização de depósitos, saques e transferências entre contas.
* **Relatórios:** Emissão do montante total do banco e montante filtrado por agência.
* **Dados:** Salvamento e carregamento automático do banco de dados utilizando arquivos JSON.

## Estrutura do Projeto

* `main.py`: Arquivo principal que gerencia o fluxo do programa, a repetição e a interface principal.
* `menu.py`: Módulo responsável por exibir a interface visual de opções no console.
* `cliente.py`: Módulo que contém a lógica de validação e armazenamento das tuplas de clientes.
* `agencia.py`: Módulo dedicado às regras de criação e busca de agências.
* `conta.py`: Módulo que abriga a lógica financeira matemática e a geração de relatórios de montante.
* `armazenamento.py`: Módulo responsável pela leitura e gravação segura dos dados no arquivo `banco.json`.