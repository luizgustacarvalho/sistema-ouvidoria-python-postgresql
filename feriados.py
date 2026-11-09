
from datetime import date, timedelta


FERIADOS_FIXOS = {
    (1, 1): "Confraternização Universal",
    (4, 21): "Tiradentes",
    (5, 1): "Dia do Trabalho",
    (9, 7): "Independência do Brasil",
    (10, 12): "Nossa Senhora Aparecida",
    (11, 2): "Finados",
    (11, 15): "Proclamação da República",
    (11, 20): "Dia Nacional de Zumbi e da Consciência Negra",
    (12, 25): "Natal"
}



EXTRA_FERIADOS = {}


def calcular_pascoa(ano):

    """
    Calcula a data da Páscoa usando o algoritmo de Meeus/Jones/Butcher.
    """

    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451

    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1

    return date(ano, mes, dia)


def obter_feriados(ano):

    """
    Retorna os feriados nacionais e as datas adicionais cadastradas.
    """

    feriados = set()

    for mes, dia in FERIADOS_FIXOS:
        feriados.add(date(ano, mes, dia))

    feriados.update(EXTRA_FERIADOS.get(ano, []))

    return feriados


def eh_dia_util(data):

    """
    Verifica se uma data é dia útil.
    """

    if data.weekday() >= 5:
        return False

    if data in obter_feriados(data.year):
        return False

    return True


def adicionar_dias_uteis(data_inicial, quantidade):

    """
    Adiciona uma quantidade de dias úteis a uma data.
    """

    data = data_inicial
    dias_contados = 0

    while dias_contados < quantidade:
        data += timedelta(days=1)

        if eh_dia_util(data):
            dias_contados += 1

    return data


def contar_dias_uteis(data_inicial, data_final):

    """
    Conta os dias úteis entre duas datas, sem incluir a data inicial.
    """

    dias_contados = 0
    data = data_inicial

    while data < data_final:
        data += timedelta(days=1)

        if eh_dia_util(data):
            dias_contados += 1

    return dias_contados
