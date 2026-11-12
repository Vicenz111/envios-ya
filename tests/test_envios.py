"""Suite de pruebas de calc() · EnvíaYa
Estudiante: 0182220060 · A=2 B=2 C=0 D=0 E=6 F=0
PMAX=40  L1=4 (incluido)  L2=10  RR=20 %  RN=40 %  V=20 %  S=$2.000
Reglas: tramo 1 peso <= 4 · fin de semana ANTES del descuento ·
        solo el MAYOR descuento · cupón inexistente se IGNORA

Los resultados esperados se calcularon a mano (informe, Parte 3).
"""
import pytest

from envios import calc

ACEPTACION = pytest.mark.aceptacion


# ---------------------------------------------------------------------------
# Casos válidos: (peso, zona, cliente, dia, cupon) -> costo esperado
# ---------------------------------------------------------------------------
CASOS_VALIDOS = [
    # R1 / R3 · valores límite del peso
    pytest.param(0.01, "urbana", "normal", 1, None, 6000, id="CP-02"),
    pytest.param(3.99, "urbana", "normal", 1, None, 6000, id="CP-04"),
    pytest.param(4, "urbana", "normal", 1, None, 6000, id="CP-05", marks=ACEPTACION),
    pytest.param(4.01, "urbana", "normal", 1, None, 9000, id="CP-06"),
    pytest.param(9.99, "urbana", "normal", 1, None, 9000, id="CP-07"),
    pytest.param(10, "urbana", "normal", 1, None, 9000, id="CP-08"),
    pytest.param(10.01, "urbana", "normal", 1, None, 9000, id="CP-09"),
    pytest.param(12.5, "urbana", "normal", 1, None, 11000, id="CP-10", marks=ACEPTACION),
    pytest.param(39.99, "urbana", "normal", 1, None, 33000, id="CP-11"),
    pytest.param(40, "urbana", "normal", 1, None, 33000, id="CP-12", marks=ACEPTACION),
    # R4 · recargo por zona
    pytest.param(6, "rural", "normal", 2, None, 10800, id="CP-15", marks=ACEPTACION),
    pytest.param(6, "nacional", "normal", 3, None, 12600, id="CP-16", marks=ACEPTACION),
    # R5 · fin de semana
    pytest.param(6, "urbana", "normal", 5, None, 9000, id="CP-20"),
    pytest.param(6, "urbana", "normal", 6, None, 11000, id="CP-21", marks=ACEPTACION),
    pytest.param(6, "urbana", "normal", 7, None, 11000, id="CP-22"),
    # R6 / R7 · tabla de decisión cliente x cupón x fin de semana
    pytest.param(6, "urbana", "frecuente", 1, None, 8600, id="CP-23", marks=ACEPTACION),
    pytest.param(6, "urbana", "frecuente", 1, "ENVIO10", 8100, id="CP-24", marks=ACEPTACION),
    pytest.param(6, "urbana", "vip", 1, "ENVIO10", 7200, id="CP-25"),
    pytest.param(6, "urbana", "normal", 6, "ENVIO10", 9900, id="CP-26"),
    pytest.param(6, "urbana", "normal", 1, "GRATIS", 9000, id="CP-27", marks=ACEPTACION),
    pytest.param(6, "urbana", "vip", 7, "DESCUENTO50", 8800, id="CP-28"),
    # R8 · mínimo y redondeo
    pytest.param(2, "urbana", "vip", 1, None, 5000, id="CP-29", marks=ACEPTACION),
    pytest.param(10.1, "urbana", "normal", 1, None, 9100, id="CP-30"),
    pytest.param(4, "rural", "vip", 6, "ENVIO10", 7400, id="CP-31", marks=ACEPTACION),
    pytest.param(12.5, "nacional", "frecuente", 7, "ENVIO10", 15700, id="CP-32"),
    pytest.param(1, "urbana", "vip", 1, "ENVIO10", 5000, id="CP-33"),
    pytest.param(12.3, "urbana", "normal", 1, None, 10800, id="CP-34"),
    pytest.param(4.5, "urbana", "normal", 1, None, 9000, id="CP-35", marks=ACEPTACION),
    # Caja blanca · caminos que no estaban en la matriz de caja negra
    pytest.param(6, "urbana", "vip", 1, None, 7200, id="CB-10"),
    pytest.param(6, "urbana", "normal", 1, "ENVIO10", 8100, id="CB-12"),
]


@pytest.mark.parametrize("peso, zona, cliente, dia, cupon, esperado", CASOS_VALIDOS)
def test_costo(peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado


# ---------------------------------------------------------------------------
# R1 · peso inválido -> ValueError("peso inválido")
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "peso",
    [
        pytest.param(0, id="CP-01", marks=ACEPTACION),
        pytest.param(-5, id="CP-03"),
        pytest.param(40.01, id="CP-13", marks=ACEPTACION),
        pytest.param(45, id="CP-14"),
    ],
)
def test_peso_invalido(peso):
    with pytest.raises(ValueError, match="peso inválido"):
        calc(peso, "urbana", "normal", 1)


# ---------------------------------------------------------------------------
# R2 · zona o día inválidos -> ValueError
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "zona, dia",
    [
        pytest.param("insular", 1, id="CP-17", marks=ACEPTACION),
        pytest.param("urbana", 0, id="CP-18", marks=ACEPTACION),
        pytest.param("urbana", 8, id="CP-19", marks=ACEPTACION),
    ],
)
def test_zona_o_dia_invalido(zona, dia):
    with pytest.raises(ValueError):
        calc(6, zona, "normal", dia)


# ---------------------------------------------------------------------------
# Caja blanca · CB-14
# v1.0.0 tenía el argumento flag (nodo 25 -> 26). En v2.0.0 se eliminó:
# la prueba ahora verifica que calc ya no imprime y que flag no se acepta.
# ---------------------------------------------------------------------------
def test_cb14_sin_flag_no_imprime(capsys):
    assert calc(6, "urbana", "normal", 1) == 9000
    assert capsys.readouterr().out == ""
    with pytest.raises(TypeError):
        calc(6, "urbana", "normal", 1, None, True)