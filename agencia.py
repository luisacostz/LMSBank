def cadastrar_agencia(agencias, numero_agencia, nome_agencia):
    nova_agencia = (numero_agencia, nome_agencia)
    agencias.append(nova_agencia)

def procurar_agencia(agencias, numero_procurado):
    for i in range(len(agencias)):
        if agencias[i][0] == numero_procurado:
            return agencias[i]
    return False

def listar_agencias(agencias):
    if len(agencias) == 0:
        print("Nenhuma agencia cadastrada.")
    else:
        print("\n--- LISTA DE AGENCIAS ---")
        for i in range(len(agencias)):
            print("Numero:", agencias[i][0])
            print("Nome:", agencias[i][1])