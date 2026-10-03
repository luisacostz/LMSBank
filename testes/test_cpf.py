from principal.cpf import validar_cpf, limpar_cpf

# Testa um CPF válido com pontuação
def test_cpf_valido_com_pontuacao():
    assert validar_cpf("529.982.247-25") == True

# Testa um CPF válido sem pontuação
def test_cpf_valido_sem_pontuacao():
    assert validar_cpf("52998224725") == True

# Testa um CPF com dígitos errados
def test_cpf_invalido():
    assert validar_cpf("529.982.247-24") == False

# Testa um CPF curto
def test_cpf_curto():
    assert validar_cpf("123456") == False

# Testa CPF com letras
def test_cpf_com_letras():
    assert validar_cpf("5299822472A") == False

# Testa números iguais
def test_cpf_numeros_iguais():
    assert validar_cpf("11111111111") == False

# Testa a limpeza da pontuação
def test_limpar_cpf():
    assert limpar_cpf("529.982.247-25") == "52998224725"