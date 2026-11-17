'''
Arquivo: test_conta.py
Descrição: Testes principais de Conta, ContaCorrente, ContaPoupanca e ContaFactory.
Rodar na raiz do projeto: python -m pytest
'''
from datetime import date

import pytest

from conta import Conta
from conta_corrente import ContaCorrente
from conta_factory import ContaFactory
from conta_poupanca import ContaPoupanca
from excecoes import SaldoInsuficienteError, TipoContaInvalidoError, ValorInvalidoError


def test_conta_abstrata_nao_pode_ser_instanciada():
    with pytest.raises(TypeError):
        Conta("1")


def test_depositar_e_valor_invalido():
    conta = ContaCorrente("1")
    conta.depositar(150.0)
    assert conta.saldo == pytest.approx(150.0)
    with pytest.raises(ValorInvalidoError):
        conta.depositar(-5)


def test_corrente_usa_cheque_especial_ate_o_limite():
    conta = ContaCorrente("1", saldo=100.0)   # disponível: 100 + 500
    conta.sacar(600.0)
    assert conta.saldo == pytest.approx(-500.0)
    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(0.01)


def test_poupanca_nao_tem_cheque_especial():
    conta = ContaPoupanca("2", saldo=100.0)
    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(100.01)


def test_transferir_ok():
    origem = ContaCorrente("1", saldo=100.0)
    destino = ContaPoupanca("2", saldo=10.0)
    origem.transferir(destino, 60.0)
    assert origem.saldo == pytest.approx(40.0)
    assert destino.saldo == pytest.approx(70.0)


def test_transferir_sem_saldo_nao_mexe_no_destino():
    origem = ContaPoupanca("2", saldo=10.0)
    destino = ContaCorrente("1")
    with pytest.raises(SaldoInsuficienteError):
        origem.transferir(destino, 50.0)
    assert destino.saldo == pytest.approx(0.0)


def test_rendimento_antes_de_um_mes_nao_rende():
    conta = ContaPoupanca("2", saldo=1000.0, ultimo_rendimento=date(2026, 10, 17))
    assert conta.aplicar_rendimento(date(2026, 11, 16)) == 0.0


def test_rendimento_de_um_mes():
    conta = ContaPoupanca("2", saldo=1000.0, ultimo_rendimento=date(2026, 10, 17))
    assert conta.aplicar_rendimento(date(2026, 11, 17)) == pytest.approx(5.0)  # 0,5%
    assert conta.ultimo_rendimento == date(2026, 11, 17)


def test_rendimento_de_tres_meses_e_composto():
    conta = ContaPoupanca("2", saldo=1000.0, ultimo_rendimento=date(2026, 8, 17))
    conta.aplicar_rendimento(date(2026, 11, 17))
    assert conta.saldo == pytest.approx(1000.0 * 1.005 ** 3, abs=0.01)


def test_factory_cria_cada_tipo_e_recusa_tipo_invalido():
    assert isinstance(ContaFactory.criar("corrente", "1"), ContaCorrente)
    assert isinstance(ContaFactory.criar("poupanca", "2"), ContaPoupanca)
    with pytest.raises(TipoContaInvalidoError):
        ContaFactory.criar("salario", "3")


def test_to_dict_e_from_dict_sao_inversos():
    for original in [ContaCorrente("1", saldo=10.0, limite=300.0),
                     ContaPoupanca("2", saldo=20.0, ultimo_rendimento=date(2026, 9, 1))]:
        copia = ContaFactory.from_dict(original.to_dict())
        assert copia.to_dict() == original.to_dict()
