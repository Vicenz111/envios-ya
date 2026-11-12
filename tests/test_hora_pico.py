"""Solicitud de cambio 2 · Hora pico (pruebas escritas ANTES de implementar).

Nuevo parámetro hora (0 a 23). Entre las 17 y las 19, inclusive, recargo del 8 %,
calculado después del recargo por zona. Si no se envía hora, no hay recargo.
"""
import pytest

from envios import calc


@pytest.mark.parametrize("peso, zona, cliente, dia, cupon, hora, esperado", [
    pytest.param(6, "urbana", "normal", 1, None, 16, 9000, id="HP-01"),
    pytest.param(6, "urbana", "normal", 1, None, 17, 9700, id="HP-02"),
    pytest.param(6, "urbana", "normal", 1, None, 18, 9700, id="HP-03"),
    pytest.param(6, "urbana", "normal", 1, None, 19, 9700, id="HP-04"),
    pytest.param(6, "urbana", "normal", 1, None, 20, 9000, id="HP-05"),
    pytest.param(6, "urbana", "normal", 1, None, 0, 9000, id="HP-06"),
    pytest.param(6, "urbana", "normal", 1, None, 23, 9000, id="HP-07"),
    pytest.param(6, "rural", "normal", 1, None, 18, 11700, id="HP-08"),
    pytest.param(6, "urbana", "normal", 6, None, 18, 11700, id="HP-09"),
    pytest.param(4, "rural", "vip", 6, "ENVIO10", 17, 7800, id="HP-10"),
])
def test_recargo_hora_pico(peso, zona, cliente, dia, cupon, hora, esperado):
    assert calc(peso, zona, cliente, dia, cupon, hora=hora) == esperado


def test_sin_hora_no_hay_recargo():  # HP-11: compatibilidad con v2.0.0
    assert calc(6, "urbana", "normal", 1) == 9000


@pytest.mark.parametrize("hora", [pytest.param(-1, id="HP-12"), pytest.param(24, id="HP-13")])
def test_hora_invalida(hora):
    with pytest.raises(ValueError, match="hora inválida"):
        calc(6, "urbana", "normal", 1, hora=hora)