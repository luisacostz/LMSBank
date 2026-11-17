class ContaCorrente:
    def __init__(self, limite: float = 500.0) -> None:
        self.limite = limite

    def saldo_disponivel(self) -> float:
        return 0.0

    def tipo(self) -> str:
        return ""
