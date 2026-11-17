'''
Arquivo: conftest.py 
Descrição: Configura o caminho das pastas "principal" e "web" para o pytest
encontrar os módulos, não importa de onde o pytest for chamado.
'''

import os
import sys

# Pasta raiz do projeto (onde este arquivo está)
raiz = os.path.dirname(os.path.abspath(__file__))

# Adiciona a raiz, "principal" e "web" ao caminho de importação do Python
for pasta in [raiz, os.path.join(raiz, "principal"), os.path.join(raiz, "web")]:
    if pasta not in sys.path:
        sys.path.append(pasta)
