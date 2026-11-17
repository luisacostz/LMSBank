class Dashboard:
    def __init__(self, num_clientes: int = 0, num_contas: int = 0, saldo_total: float = 0.0, saldo_medio: float = 0.0, maior_saldo: float = 0.0, maior_saldo_conta: str = "", menor_saldo: float = 0.0, menor_saldo_conta: str = "") -> None:
        self.num_clientes = num_clientes
        self.num_contas = num_contas
        self.saldo_total = saldo_total
        self.saldo_medio = saldo_medio
        self.maior_saldo = maior_saldo
        self.maior_saldo_conta = maior_saldo_conta
        self.menor_saldo = menor_saldo
        self.menor_saldo_conta = menor_saldo_conta
