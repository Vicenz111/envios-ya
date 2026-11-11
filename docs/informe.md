# Parcial 3 · Ingeniería de Software I — EnvíaYa

**Estudiante:** _vicente rivadeneira_
**Código estudiantil:** 0182220060
**Repositorio:** https://github.com/Vicenz111/envios-ya

## Mis parámetros

Últimos 6 dígitos del código: **220060**

| A | B | C | D | E | F | PMAX   | L1   | L2    | RR   | RN   | V    | S      | CAMBIO |
|---|---|---|---|---|---|------  |----  |----   |----  |----  |---   |---     |--------|
| 2 | 2 | 0 | 0 | 6 | 0 | 40 kg  | 4 kg | 10 kg | 20 % | 40 % | 20 % | $2.000 | 2 (hora pico) |

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

---

## Parte 2 · Plan de pruebas

### 2.1 Alcance

**Objeto de prueba:** la función `calc` del módulo `envios.py` en el código heredado (v1.0.0) y en las versiones que salgan después de la corrección, la refactorización y la solicitud de cambio.

**Dentro del alcance**

- Las reglas de negocio R1 a R8 con los parámetros del estudiante 0182220060 (PMAX = 40, L1 = 4, L2 = 10, RR = 20 %, RN = 40 %, V = 20 %, S = $2.000).
- Las validaciones de entrada (peso, zona, día) y los errores que se lanzan.
- La interacción de cliente, cupón y fin de semana (reglas B, E y F).
- La solicitud de cambio de la Parte 8 (recargo de hora pico).
- Las pruebas de regresión después de cada corrección y de la refactorización.

**Fuera del alcance**

- Interfaz gráfica, base de datos, facturación y demás módulos de EnvíaYa.
- Pruebas de rendimiento, carga y seguridad.
- Tipos de cliente distintos de normal, frecuente y VIP (ver supuesto S1).

### 2.2 Niveles de prueba aplicados a este caso

| Nivel | Qué se prueba en EnvíaYa | Cómo se aplica | Técnica |
|---|---|---|---|
| **Unidad** | Cada función por separado. Antes del refactor: `calc`. Después: `tarifa_base`, `recargo_zona`, `recargo_fin_de_semana`, `aplicar_descuento`, `redondear` y cada clase Estrategia. | Pruebas `pytest` parametrizadas que llaman a una sola función con entradas controladas. | Caja negra (particiones, valores límite) y caja blanca (caminos, ramas). |
| **Integración** | Que las funciones extraídas y las estrategias trabajen juntas en el orden correcto: base → zona → fin de semana → descuento → mínimo → redondeo. | Integración ascendente (bottom-up): primero se prueban las piezas y después la función principal `calcular_costo`, que las compone. Casos que combinan varias reglas a la vez (ej. 4 kg, rural, VIP, sábado, ENVIO10 = $7.400). | Tabla de decisión, casos combinados. |
| **Sistema** | El módulo completo contra toda la especificación R1–R8, incluido el manejo de errores, como lo usaría el sistema de EnvíaYa. | Ejecución de la suite completa desde la terminal con medición de cobertura: `pytest -v --cov=envios --cov-branch`. Se repite como regresión después de cada `merge`. | Matriz completa de casos (mínimo 20). |
| **Aceptación** | Que se cumplan los criterios Dado / Cuando / Entonces de HU-01, HU-02 y HU-03. | Cada criterio de aceptación se automatiza como prueba marcada `@pytest.mark.aceptacion`. El dueño del producto (EnvíaYa, representado por el docente) los valida en la sustentación. | Pruebas basadas en historias de usuario. |

### 2.3 Estrategia, ambiente y roles

**Estrategia**

1. **Basada en riesgos y en requisitos:** cada regla R1–R8 tiene al menos un caso de prueba (matriz de trazabilidad), y las reglas que dependen de mi código estudiantil (tramo 1, fin de semana, cliente + cupón, cupón inexistente) se prueban con más casos.
2. **Caja negra primero:** particiones de equivalencia, valores límite y tabla de decisión (Parte 3). El resultado esperado se calcula a mano, sin mirar el código.
3. **Caja blanca después:** grafo de flujo, complejidad ciclomática, caminos independientes y cobertura de sentencias y ramas (Parte 4).
4. **Automatización total** con `pytest` y `@pytest.mark.parametrize`. Todas las pruebas se ejecutan primero contra v1.0.0 para dejar evidencia de los defectos.
5. **Corrección guiada por pruebas:** cada defecto se corrige en su propia rama `fix/DEF-xx`, con la prueba que lo reproduce fallando antes de corregir.
6. **Regresión:** la suite completa se ejecuta después de cada corrección, de la refactorización y de cada `merge` a `main`.

**Ambiente**

| Elemento | Detalle |
|---|---|
| Sistema operativo | Windows (equipo del estudiante) |
| Lenguaje | Python 3 en entorno virtual `.venv` |
| Herramientas de prueba | `pytest`, `pytest-cov` (versiones fijadas en `requirements.txt`) |
| Editor | Visual Studio Code |
| Control de versiones | Git + GitHub (repositorio `envios-ya`) |
| Datos de prueba | Tabla de casos de la Parte 3 con resultados esperados calculados a mano |
| Comando de ejecución | `pytest -v --cov=envios --cov-branch --cov-report=term-missing --cov-report=html` |

**Roles** _(en este parcial una misma persona los cumple todos)_

| Rol | Responsabilidad |
|---|---|
| Líder de calidad | Elabora el plan, define criterios de entrada y salida, calcula las métricas. |
| Analista de pruebas | Diseña los casos de caja negra y caja blanca y calcula los resultados esperados. |
| Ingeniero de automatización | Implementa la suite en `pytest` y mide la cobertura. |
| Desarrollador de mantenimiento | Corrige los defectos, refactoriza e implementa la solicitud de cambio. |
| Gestor de configuración | Administra ramas, etiquetas, versionado semántico y CHANGELOG. |
| Dueño del producto (EnvíaYa / docente) | Aprueba la especificación y acepta la versión final en la sustentación. |

### 2.4 Riesgos y mitigación

| ID | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| RG-01 | Un resultado esperado mal calculado a mano produce una prueba falsa (falla un código correcto o pasa uno incorrecto). | Media | Alto | Cálculo paso a paso documentado en el informe; verificación cruzada con el ejemplo del enunciado ($7.400). |
| RG-02 | Errores de punto flotante en porcentajes y redondeo (ej. 8.549,999… en lugar de 8.550). | Media | Alto | Casos justo en el borde del redondeo ($50); en el código corregido, redondeo explícito y controlado. |
| RG-03 | Ambigüedades en la especificación (cliente no listado, texto del mensaje de error). | Media | Medio | Supuestos S1 y S2 documentados en la Parte 1; las pruebas de error verifican el tipo de excepción. |
| RG-04 | La refactorización introduce regresiones. | Media | Alto | Refactorizar solo con la suite en verde, en commits pequeños, y ejecutar la regresión completa después de cada paso. |
| RG-05 | Quitar el argumento `flag` rompe el código que llama a `calc`. | Alta | Medio | Versión MAJOR según versionado semántico y nota en el CHANGELOG. |
| RG-06 | Conflictos al integrar las ramas `fix/DEF-xx`. | Media | Medio | Ramas cortas, integración frecuente a `main` y regresión después de cada `merge`. |
| RG-07 | El tiempo no alcanza (la entrega es el mismo día). | Alta | Alto | Priorizar los defectos por severidad; usar `parametrize` para automatizar rápido; commits a lo largo del día. |
| RG-08 | El ambiente de la sustentación es distinto al del desarrollo. | Baja | Alto | `requirements.txt`, entorno virtual e instrucciones de ejecución en el README. |

### 2.5 Criterios de entrada y de salida

**Criterios de entrada** (para empezar a ejecutar pruebas)

- La especificación R1–R8 está escrita con mis parámetros y verificada contra el código estudiantil.
- El código heredado está en el repositorio con la etiqueta `v1.0.0` y el `CONFIG` lleno.
- El ambiente está instalado: `.venv`, `pytest` y `pytest-cov` funcionando.
- Los casos de prueba de la Parte 3 están diseñados y cada uno tiene su resultado esperado calculado a mano.

**Criterios de salida** (para dar por terminada la prueba y publicar la versión)

- El 100 % de los casos diseñados se ejecutaron.
- El 100 % de los casos pasan en la versión final.
- Todos los defectos reportados están corregidos y cerrados (0 defectos abiertos de severidad crítica o alta).
- La cobertura de sentencias es del 100 % y la de ramas al menos del 95 % sobre el código final.
- Cada requisito R1–R8 tiene al menos un caso de prueba en la matriz de trazabilidad.
- La regresión está en verde después del último `merge`, y la versión está etiquetada y documentada en el CHANGELOG.

**Criterios de suspensión:** se detiene la ejecución si el ambiente no permite importar el módulo o si se encuentra un error en la especificación. Se reanuda cuando se corrige.
