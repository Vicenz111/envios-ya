"""Pruebas de unidad de las funciones extraídas y de las estrategias de zona (v2.0.0)."""
import pytest

from envios import (ZONAS, EstrategiaZona, ZonaNacional, ZonaRural, ZonaUrbana,
                    obtener_estrategia_zona, porcentaje_descuento,
                    recargo_fin_de_semana, redondear, tarifa_base)


@pytest.mark.parametrize("peso, esperado", [(4, 6000), (4.01, 9000), (10, 9000), (12.5, 11000)])
def test_tarifa_base(peso, esperado):
    assert tarifa_base(peso) == pytest.approx(esperado)


@pytest.mark.parametrize("estrategia, esperado", [
    (ZonaUrbana(), 9000), (ZonaRural(), 10800), (ZonaNacional(), 12600)])
def test_estrategias_de_zona(estrategia, esperado):
    assert isinstance(estrategia, EstrategiaZona)
    assert estrategia.aplicar_recargo(9000) == pytest.approx(esperado)


def test_registro_de_zonas():
    assert set(ZONAS) == {"urbana", "rural", "nacional"}
    with pytest.raises(ValueError, match="zona inválida"):
        obtener_estrategia_zona("insular")


@pytest.mark.parametrize("dia, esperado", [(5, 0), (6, 2000), (7, 2000)])
def test_recargo_fin_de_semana(dia, esperado):
    assert recargo_fin_de_semana(dia) == esperado


@pytest.mark.parametrize("cliente, cupon, esperado", [
    ("normal", None, 0.0), ("frecuente", None, 0.05), ("vip", None, 0.20),
    ("frecuente", "ENVIO10", 0.10), ("vip", "ENVIO10", 0.20), ("normal", "GRATIS", 0.0)])
def test_porcentaje_descuento_toma_el_mayor(cliente, cupon, esperado):
    assert porcentaje_descuento(cliente, cupon) == esperado


@pytest.mark.parametrize("costo, esperado", [
    (8550, 8600), (8549.99, 8500), (9080, 9100), (10840, 10800), (8549.999999999998, 8600)])
def test_redondear(costo, esperado):
    assert redondear(costo) == esperado


def test_estrategia_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        EstrategiaZona()