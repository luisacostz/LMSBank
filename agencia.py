def cadastrar_agencia(agencias, numero_agencia, nome_agencia):
  nova_agencia = [numero_agencia, nome_agencia]
  agencias.append(nova_agencia)

def listar_agencias(agencias):
  if len(agencias) == 0:
    print('Nenhuma agência cadastrada.')
  else:
    print('\n--- LISTA DE AGÊNCIAS ---')
    for agencia in agencias:
      print('Número de agência:', agencia[0], '- Nome:', agencia[1])

def procurar_agencia(agencias, numero_procurado):
  for agencia in agencias:
    if agencia[0] == numero_procurado:
      return agencia
  return None
