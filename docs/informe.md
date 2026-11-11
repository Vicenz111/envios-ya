# Parcial 3 · Ingeniería de Software I — EnvíaYa

**Estudiante:** _(tu nombre completo)_
**Código estudiantil:** 0182220060
**Repositorio:** https://github.com/TU_USUARIO/envios-ya

## Mis parámetros

Últimos 6 dígitos del código: **220060**

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 2 | 2 | 0 | 0 | 6 | 0 | 40 kg | 4 kg | 10 kg | 20 % | 40 % | 20 % | $2.000 | 2 (hora pico) |

| Parámetro | Fórmula | Cálculo | Valor |
|---|---|---|---|
| PMAX | 30 + 5·A | 30 + 5·2 | 40 kg |
| L1 | 2 + (B mod 3) | 2 + (2 mod 3) = 2 + 2 | 4 kg |
| L2 | 10 + C | 10 + 0 | 10 kg |
| RR | 10 + 5·(E mod 4) | 10 + 5·(6 mod 4) = 10 + 5·2 | 20 % |
| RN | 40 + 5·(F mod 3) | 40 + 5·(0 mod 3) = 40 + 0 | 40 % |
| V | 10 + 5·(A mod 3) | 10 + 5·(2 mod 3) = 10 + 5·2 | 20 % |
| S | 2000 + 500·(C mod 4) | 2000 + 500·0 | $2.000 |
| CAMBIO | (A + F) mod 3 | (2 + 0) mod 3 | 2 |

**Reglas según paridad**

| Dígito | Valor | Paridad | Regla que me corresponde |
|---|---|---|---|
| D · tramo 1 | 0 | par | Incluye el límite: **peso ≤ 4** |
| E · recargo fin de semana | 6 | par | Se suma **antes** de los descuentos |
| B · cliente y cupón | 2 | par | Solo se aplica **el mayor** de los dos descuentos |
| F · cupón que no existe | 0 | par | **Se ignora** |

---

## Parte 1 · Requisitos y criterios de aceptación

### 1.1 Especificación completa (con mis valores)

La función recibe: `peso` en kg (puede tener decimales); `zona` ∈ {urbana, rural, nacional}; `cliente` ∈ {normal, frecuente, vip}; `dia` de 1 a 7 (6 = sábado, 7 = domingo); `cupon` opcional.

| ID | Regla |
|---|---|
| **R1** | El peso debe cumplir **0 < peso ≤ 40**. Si no, se lanza el error "peso inválido". |
| **R2** | Si la zona no es urbana, rural ni nacional, o el día no está entre 1 y 7 (inclusive), se lanza un error. |
| **R3** | Tarifa base. Tramo 1: **peso ≤ 4** → $6.000. Tramo 2: **4 < peso ≤ 10** → $9.000. Más de 10 kg: **$9.000 + $800 × (peso − 10)**, proporcional (ej. 12,5 kg → 9.000 + 2,5 × 800 = $11.000). |
| **R4** | Recargo por zona sobre la tarifa base. Rural: **+20 %**. Nacional: **+40 %**. Urbana: sin recargo. |
| **R5** | Si el día es 6 (sábado) o 7 (domingo) se suman **$2.000**, **antes** de aplicar los descuentos (después del recargo por zona). |
| **R6** | Descuentos. Cliente frecuente: **5 %**. Cliente VIP: **20 %**. Cupón ENVIO10: **10 %**. Si el cliente tiene descuento y además trae cupón, **solo se aplica el mayor de los dos** (no se acumulan). |
| **R7** | Un cupón que no existe (cualquier valor distinto de ENVIO10) **se ignora**: se calcula como si no hubiera cupón. |
| **R8** | El costo nunca es menor que **$5.000**. El resultado se redondea al múltiplo de $100 más cercano; los $50 redondean hacia arriba (ej. $8.550 → $8.600; $8.549 → $8.500). |

**Orden del cálculo:** tarifa base (R3) → recargo por zona (R4) → recargo de fin de semana (R5) → descuento (R6, R7) → mínimo $5.000 (R8) → redondeo (R8).

**Supuestos documentados**

- S1. La especificación no define qué pasa con un tipo de cliente no listado; se asume que se trata como cliente normal (sin descuento) y no se considera defecto.
- S2. Aplicar el mínimo antes o después del redondeo da el mismo resultado (cualquier valor ≥ 5.000 redondea a ≥ 5.000), así que se respeta el orden de R8.

**Ejemplo calculado a mano con mis valores**

Entradas: peso = 4 kg · zona = rural · cliente = vip · día = 6 (sábado) · cupón = ENVIO10

1. D = 0 es par: el tramo 1 es peso ≤ 4. Como 4 ≤ 4 → tramo 1 → **$6.000**
2. Zona rural +20 % → 6.000 × 1,20 = **$7.200**
3. Sábado, y E = 6 es par: el recargo va antes de los descuentos → 7.200 + 2.000 = **$9.200**
4. B = 2 es par: solo el mayor descuento. VIP 20 % contra cupón 10 % → 9.200 × 0,80 = **$7.360**
5. Es mayor que $5.000. Se redondea a $100 → **resultado esperado: $7.400**

### 1.2 Historias de usuario

#### HU-01 · Validar los datos del envío (cubre R1, R2)

> **Como** asesor de ventas de EnvíaYa,
> **quiero** que el sistema rechace los envíos con datos inválidos,
> **para** no cotizar envíos que la empresa no puede despachar.

| ID | Dado | Cuando | Entonces |
|---|---|---|---|
| CA-01.1 | un envío de 0 kg a zona urbana, cliente normal, día 1 | se calcula el costo | el sistema lanza el error "peso inválido" |
| CA-01.2 | un envío de 40,01 kg (más que PMAX = 40) | se calcula el costo | el sistema lanza el error "peso inválido" |
| CA-01.3 | un envío de exactamente 40 kg, urbana, normal, día 1 | se calcula el costo | el sistema lo acepta y devuelve $33.000 |
| CA-01.4 | un envío con zona "insular" | se calcula el costo | el sistema lanza un error de zona inválida |
| CA-01.5 | un envío con día 0 o día 8 | se calcula el costo | el sistema lanza un error de día inválido |

#### HU-02 · Calcular la tarifa según peso, zona y día (cubre R3, R4, R5)

> **Como** cliente de EnvíaYa,
> **quiero** que el costo dependa del peso del paquete, la zona de destino y el día del envío,
> **para** pagar un precio justo y que pueda prever.

| ID | Dado | Cuando | Entonces |
|---|---|---|---|
| CA-02.1 | un paquete de 4 kg, urbana, normal, día 1 | se calcula el costo | se cobra tramo 1 (el límite está incluido): $6.000 |
| CA-02.2 | un paquete de 4,5 kg, urbana, normal, día 1 | se calcula el costo | se cobra tramo 2: $9.000 |
| CA-02.3 | un paquete de 12,5 kg, urbana, normal, día 1 | se calcula el costo | se cobra 9.000 + 2,5 × 800 = $11.000 |
| CA-02.4 | un paquete de 6 kg, rural, normal, día 2 | se calcula el costo | se aplica +20 %: $10.800 |
| CA-02.5 | un paquete de 6 kg, nacional, normal, día 3 | se calcula el costo | se aplica +40 %: $12.600 |
| CA-02.6 | un paquete de 6 kg, urbana, normal, día 6 (sábado) | se calcula el costo | se suman $2.000: $11.000 (igual el domingo, día 7) |

#### HU-03 · Aplicar descuentos, cupón, mínimo y redondeo (cubre R6, R7, R8)

> **Como** cliente frecuente o VIP de EnvíaYa,
> **quiero** que se me aplique el mejor descuento al que tengo derecho y que el valor final sea redondo,
> **para** pagar lo correcto sin cobros por debajo del mínimo ni valores con centavos.

| ID | Dado | Cuando | Entonces |
|---|---|---|---|
| CA-03.1 | 4 kg, rural, VIP, sábado, cupón ENVIO10 | se calcula el costo | solo se aplica el mayor descuento (VIP 20 %): $7.400 |
| CA-03.2 | 6 kg, urbana, frecuente, día 1, cupón ENVIO10 | se calcula el costo | gana el cupón (10 % > 5 %): $8.100 |
| CA-03.3 | 6 kg, urbana, normal, día 1, cupón "GRATIS" | se calcula el costo | el cupón se ignora: $9.000 |
| CA-03.4 | 2 kg, urbana, VIP, día 1 (6.000 × 0,8 = $4.800) | se calcula el costo | se cobra el mínimo: $5.000 |
| CA-03.5 | 6 kg, urbana, frecuente, día 1 (9.000 × 0,95 = $8.550) | se calcula el costo | los $50 redondean hacia arriba: $8.600 |

### 1.3 Matriz de trazabilidad

_(La columna de casos de prueba se completa en la Parte 3.)_

| Requisito | Historia | Criterios de aceptación | Casos de prueba |
|---|---|---|---|
| R1 · Peso válido (0 < p ≤ 40) | HU-01 | CA-01.1, CA-01.2, CA-01.3 | _pendiente Parte 3_ |
| R2 · Zona y día válidos | HU-01 | CA-01.4, CA-01.5 | _pendiente Parte 3_ |
| R3 · Tarifa base por tramos | HU-02 | CA-02.1, CA-02.2, CA-02.3 | _pendiente Parte 3_ |
| R4 · Recargo por zona | HU-02 | CA-02.4, CA-02.5 | _pendiente Parte 3_ |
| R5 · Recargo fin de semana | HU-02 | CA-02.6, CA-03.1 | _pendiente Parte 3_ |
| R6 · Descuento cliente/cupón | HU-03 | CA-03.1, CA-03.2, CA-03.5 | _pendiente Parte 3_ |
| R7 · Cupón inexistente | HU-03 | CA-03.3 | _pendiente Parte 3_ |
| R8 · Mínimo y redondeo | HU-03 | CA-03.4, CA-03.5 | _pendiente Parte 3_ |
