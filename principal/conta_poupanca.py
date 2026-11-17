'''
Módulo: conta_poupanca.py
Descrição: Conta poupança. Rende todo MÊS. A conta lembra até que dia o rendimento
já foi pago (ultimo_rendimento) e, ao aplicar, paga os meses completos que faltam.
'''

from __future__ import annotations # para usar ContaPoupanca como tipo de retorno de from_dict()
import calendar # para calendar.monthrange() no somar_meses()
from datetime import date # para guardar a data do último rendimento
from typing import TYPE_CHECKING # para evitar import circular
from conta import Conta # Classe abstrata Conta, que define o que é comum a todas as contas e o fluxo das operações.

# Será usado apenas para type hinting, não para criar objetos.
if TYPE_CHECKING:
    from agencia import Agencia
    from cliente import Cliente

TAXA_PADRAO = 0.005  # 0,8% ao mês

# Função auxiliar para somar meses a uma data. Se o dia não existir no mês de destino, usa o último dia.
def somar_meses(data: date, meses: int) -> date:
    total = data.month - 1 + meses
    ano = data.year + total // 12
    mes = total % 12 + 1 
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia)

# Classe ContaPoupanca.
class ContaPoupanca(Conta):
    def __init__(self, numero: str, saldo: float = 0.0, cliente: Cliente = None,
                 agencia: Agencia = None, taxa_rendimento: float = TAXA_PADRAO,
                 ultimo_rendimento: date = None) -> None:
        super().__init__(numero, saldo, cliente, agencia)
        self.taxa_rendimento = taxa_rendimento                    # taxa MENSAL
        self.ultimo_rendimento = ultimo_rendimento or date.today()  # conta nova começa hoje

    # Saldo disponível é o que a conta pode gastar agora (a poupança não tem cheque especial).
    def saldo_disponivel(self) -> float:
        return self.saldo

    # O tipo da conta é usado no JSON e na exibição para o usuário.
    def tipo(self) -> str:
        return "poupanca"

    # Aplica o rendimento da poupança, se já passou um mês completo desde o último rendimento (juros compostos).
    def aplicar_rendimento(self, hoje: date = None) -> float:
        # Se não passar nenhum argumento, considera hoje como data de referência.
        hoje = hoje or date.today()
        # Conta quantos meses completos já passaram.
        meses = 0
        # Avança mês a mês, até que o próximo mês seja maior que hoje.
        while somar_meses(self.ultimo_rendimento, meses + 1) <= hoje:
            meses += 1
        if meses == 0:
            return 0.0
        # Calcula o rendimento composto: saldo * ((1 + taxa) ** meses - 1)
        ganho = round(self.saldo * ((1 + self.taxa_rendimento) ** meses - 1), 2)
        self.saldo += ganho
        # Avança só os meses pagos: os dias que sobraram contam para o próximo rendimento.
        self.ultimo_rendimento = somar_meses(self.ultimo_rendimento, meses)
        return ganho

    # Conversão para o JSON. Adiciona a taxa de rendimento e a data do último rendimento ao dicionário.
    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["taxa_rendimento"] = self.taxa_rendimento
        dados["ultimo_rendimento"] = self.ultimo_rendimento.isoformat() 
        return dados

    # Cria uma conta poupança a partir de um dicionário. O cliente e a agência podem ser passados como argumentos.
    @classmethod
    def from_dict(cls, dados: dict, cliente: Cliente = None,
                  agencia: Agencia = None) -> ContaPoupanca:
        texto = dados.get("ultimo_rendimento")
        # Poupança antiga, sem a data no JSON: começa a contar de hoje.
        ultimo = date.fromisoformat(texto) if texto else None
        return cls(
            numero=dados["numero"],
            saldo=dados.get("saldo", 0.0),
            cliente=cliente,
            agencia=agencia,
            taxa_rendimento=dados.get("taxa_rendimento", TAXA_PADRAO),
            ultimo_rendimento=ultimo,
        )
