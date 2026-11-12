"""envios.py · Cálculo del costo de un envío de EnvíaYa.

Especificación del estudiante 0182220060 (A=2 B=2 C=0 D=0 E=6 F=0).
"""
import math
from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Constantes del negocio (antes eran números mágicos)
# ---------------------------------------------------------------------------
PESO_MAXIMO = 40                 # PMAX (kg)
LIMITE_TRAMO_1 = 4               # L1 (kg), incluido: peso <= 4
LIMITE_TRAMO_2 = 10              # L2 (kg), incluido: peso <= 10
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
VALOR_KG_ADICIONAL = 800         # por cada kg sobre L2, proporcional

RECARGO_RURAL = 0.20             # RR
RECARGO_NACIONAL = 0.40          # RN

DIAS_VALIDOS = range(1, 8)       # 1 a 7
DIAS_FIN_DE_SEMANA = (6, 7)      # sábado y domingo
RECARGO_FIN_DE_SEMANA = 2000     # S, se suma ANTES de los descuentos (E par)

HORAS_VALIDAS = range(0, 24)     # 0 a 23
HORA_PICO_INICIO = 17            # inclusive
HORA_PICO_FIN = 19               # inclusive
RECARGO_HORA_PICO = 0.08         # después del recargo por zona

DESCUENTOS_CLIENTE = {"normal": 0.0, "frecuente": 0.05, "vip": 0.20}  # V = 20 %
CUPONES = {"ENVIO10": 0.10}      # un cupón que no existe se ignora (F par)

COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100


# ---------------------------------------------------------------------------
# Patrón Estrategia: recargo por zona
# ---------------------------------------------------------------------------
class EstrategiaZona(ABC):
    """Define cómo una zona modifica la tarifa base."""

    @abstractmethod
    def aplicar_recargo(self, tarifa: float) -> float:
        ...


class ZonaUrbana(EstrategiaZona):
    def aplicar_recargo(self, tarifa: float) -> float:
        return tarifa


class ZonaRural(EstrategiaZona):
    def aplicar_recargo(self, tarifa: float) -> float:
        return tarifa * (1 + RECARGO_RURAL)


class ZonaNacional(EstrategiaZona):
    def aplicar_recargo(self, tarifa: float) -> float:
        return tarifa * (1 + RECARGO_NACIONAL)


ZONAS = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# ---------------------------------------------------------------------------
# Funciones extraídas
# ---------------------------------------------------------------------------
def validar_peso(peso: float) -> None:
    if not 0 < peso <= PESO_MAXIMO:
        raise ValueError("peso inválido")


def obtener_estrategia_zona(zona: str) -> EstrategiaZona:
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    return ZONAS[zona]


def validar_dia(dia: int) -> None:
    if dia not in DIAS_VALIDOS:
        raise ValueError("día inválido")


def validar_hora(hora: int | None) -> None:
    if hora is not None and hora not in HORAS_VALIDAS:
        raise ValueError("hora inválida")


def aplicar_recargo_hora_pico(costo: float, hora: int | None) -> float:
    if hora is not None and HORA_PICO_INICIO <= hora <= HORA_PICO_FIN:
        return costo * (1 + RECARGO_HORA_PICO)
    return costo


def tarifa_base(peso: float) -> float:
    if peso <= LIMITE_TRAMO_1:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2) * VALOR_KG_ADICIONAL


def recargo_fin_de_semana(dia: int) -> int:
    return RECARGO_FIN_DE_SEMANA if dia in DIAS_FIN_DE_SEMANA else 0


def porcentaje_descuento(cliente: str, cupon: str | None) -> float:
    """Solo se aplica el mayor entre el descuento del cliente y el del cupón."""
    descuento_cliente = DESCUENTOS_CLIENTE.get(cliente, 0.0)
    descuento_cupon = CUPONES.get(cupon, 0.0)
    return max(descuento_cliente, descuento_cupon)


def redondear(costo: float) -> int:
    """Múltiplo de 100 más cercano; los 50 redondean hacia arriba."""
    costo = round(costo, 2)  # elimina el ruido de punto flotante
    return math.floor(costo / MULTIPLO_REDONDEO + 0.5) * MULTIPLO_REDONDEO


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------
def calcular_costo(peso: float, zona: str, cliente: str, dia: int,
                   cupon: str | None = None, *, hora: int | None = None) -> int:
    validar_peso(peso)
    estrategia_zona = obtener_estrategia_zona(zona)
    validar_dia(dia)
    validar_hora(hora)

    costo = estrategia_zona.aplicar_recargo(tarifa_base(peso))
    costo = aplicar_recargo_hora_pico(costo, hora)
    costo += recargo_fin_de_semana(dia)
    costo *= 1 - porcentaje_descuento(cliente, cupon)
    costo = max(costo, COSTO_MINIMO)
    return redondear(costo)


# Nombre anterior, conservado para quienes ya llaman a calc()
calc = calcular_costo