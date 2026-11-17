class ContaPoupanca:
    def __init__(self, taxa_rendimento: float = 0.01) -> None:
        self.taxa_rendimento = taxa_rendimento

    def saldo_disponivel(self) -> float:
        return 0.0

    def aplicar_rendimento(self) -> float:
        return 0.0

    def tipo(self) -> str:
        return ""
