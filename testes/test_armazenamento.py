"""
Módulo: test_armazenamento.py
Descrição: Testes automatizados para validar a leitura, gravação, codificação e sobrescrita de dados no arquivo JSON.
"""

# Importa o módulo json e as funções de persistência testadas
import json

from armazenamento import gravar_json, ler_json


# Verifica se a leitura de um arquivo inexistente retorna a estrutura inicial padrão vazia
def test_ler_arquivo_inexistente_devolve_estrutura_vazia(tmp_path):
    dados = ler_json(str(tmp_path / "nao_existe.json"))
    assert dados == {"agencia": None, "clientes": [], "contas": []}


# Verifica se os dados gravados no JSON são recuperados exatamente iguais na leitura
def test_gravar_e_ler_devolvem_os_mesmos_dados(tmp_path):
    caminho = str(tmp_path / "banco.json")
    dados = {
        "agencia": {"numero_agencia": "0001", "nome": "Sede"},
        "clientes": [{"nome": "Maria Conceição", "cpf": "52998224725"}],
        "contas": [{"numero": "1", "saldo": 10.5}],
    }
    gravar_json(dados, caminho)
    assert ler_json(caminho) == dados


# Verifica se caracteres acentuados são salvos diretamente em UTF-8 sem escapar caracteres
def test_gravar_mantem_acentos_legiveis(tmp_path):
    caminho = tmp_path / "banco.json"
    gravar_json({"nome": "Conceição"}, str(caminho))
    assert "Conceição" in caminho.read_text(encoding="utf-8")


# Verifica se uma nova gravação sobrescreve completamente o conteúdo anterior do arquivo
def test_gravar_substitui_o_conteudo_anterior(tmp_path):
    caminho = str(tmp_path / "banco.json")
    gravar_json({"clientes": [1, 2, 3]}, caminho)
    gravar_json({"clientes": []}, caminho)
    assert ler_json(caminho) == {"clientes": []}


# Verifica se a função ler_json carrega corretamente qualquer estrutura JSON válida existente
def test_ler_devolve_o_json_cru(tmp_path):
    caminho = tmp_path / "banco.json"
    caminho.write_text(json.dumps({"x": 1}), encoding="utf-8")
    assert ler_json(str(caminho)) == {"x": 1}
