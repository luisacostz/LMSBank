'''
Arquivo: conftest.py
Descrição: Configura o caminho dos módulos para o pytest encontrar as pastas
"principal" e "web" ao rodar os testes, não importa de onde o pytest for chamado.
'''

# Configura o caminho dos módulos para o pytest encontrar as pastas "principal" e "web" ao rodar os testes, não importa de onde o pytest for chamado.
import os
import sys

# Pasta raiz do projeto
raiz = os.path.dirname(os.path.abspath(__file__))

# Adiciona as pastas "principal" e "web" ao sys.path para que o pytest possa importar os módulos corretamente.
for pasta in [raiz, os.path.join(raiz, "principal"), os.path.join(raiz, "web")]:
    if pasta not in sys.path:
        sys.path.append(pasta)