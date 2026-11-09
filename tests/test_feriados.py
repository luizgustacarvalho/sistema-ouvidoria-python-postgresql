
from datetime import date

from feriados import eh_dia_util, adicionar_dias_uteis


def test_sabado_nao_e_dia_util():
    assert eh_dia_util(date(2026, 11, 7)) is False


def test_domingo_nao_e_dia_util():
    assert eh_dia_util(date(2026, 11, 8)) is False


def test_feriado_nacional_nao_e_dia_util():
    assert eh_dia_util(date(2026, 11, 20)) is False


def test_segunda_feira_e_dia_util():
    assert eh_dia_util(date(2026, 11, 9)) is True


def test_calcular_cinco_dias_uteis():
    resultado = adicionar_dias_uteis(
        date(2026, 11, 6),
        5
    )

    assert resultado == date(2026, 11, 13)


def test_pular_feriado_durante_contagem():
    resultado = adicionar_dias_uteis(
        date(2026, 11, 19),
        1
    )

    assert resultado == date(2026, 11, 23)
