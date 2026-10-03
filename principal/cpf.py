
'''
Módulo: cpf.py
Projeto: LMSBank
Descrição: Contém funções para limpar e validar
CPFs usando os dígitos verificadores.
'''


# Remove a pontuação do CPF, deixando apenas os números
def limpar_cpf(cpf):
    # Remove os pontos
    cpf = cpf.replace(".", "")

    # Remove os traços
    cpf = cpf.replace("-", "")

    # Remove espaços
    cpf = cpf.replace(" ", "")

    # Devolve o CPF sem pontuação
    return cpf


# Verifica se o CPF informado é válido
def validar_cpf(cpf):
    # Primeiro, remove a pontuação do CPF
    cpf = limpar_cpf(cpf)

    # Um CPF precisa ter exatamente 11 caracteres
    if len(cpf) != 11:
        return False

    # Verifica se todos os caracteres são números
    if not cpf.isdigit():
        return False

    # Verifica se todos os números são iguais
    # Exemplos: 11111111111 ou 00000000000
    if cpf == cpf[0] * 11:
        return False

    # Cria uma lista para guardar cada número do CPF
    numeros = []

    # Percorre cada caractere do CPF
    for numero in cpf:
        # Converte o caractere para inteiro
        # e adiciona o número à lista
        numeros.append(int(numero))

    # ---------------------------------
    # Cálculo do primeiro dígito verificador
    # ---------------------------------

    # Começa a soma em zero
    soma = 0

    # Percorre os 9 primeiros números do CPF
    for i in range(9):
        # Multiplica cada número pelo peso correspondente
        # Os pesos vão de 10 até 2
        soma = soma + numeros[i] * (10 - i)

    # Divide a soma por 11 e guarda o resto
    resto = soma % 11

    # Se o resto for 0 ou 1, o dígito é zero
    if resto < 2:
        digito1 = 0
    else:
        # Caso contrário, subtrai o resto de 11
        digito1 = 11 - resto

    # Compara o dígito calculado com o 10º número
    if digito1 != numeros[9]:
        return False

    # ---------------------------------
    # Cálculo do segundo dígito verificador
    # ---------------------------------

    # Começa uma nova soma em zero
    soma = 0

    # Percorre os 10 primeiros números,
    # incluindo o primeiro dígito calculado
    for i in range(10):
        # Multiplica cada número pelo peso correspondente
        # Os pesos vão de 11 até 2
        soma = soma + numeros[i] * (11 - i)

    # Divide a soma por 11 e guarda o resto
    resto = soma % 11

    # Se o resto for 0 ou 1, o dígito é zero
    if resto < 2:
        digito2 = 0
    else:
        # Caso contrário, subtrai o resto de 11
        digito2 = 11 - resto

    # Compara o dígito calculado com o último número
    if digito2 != numeros[10]:
        return False

    # Se passou por todas as verificações,
    # o CPF é válido
    return True