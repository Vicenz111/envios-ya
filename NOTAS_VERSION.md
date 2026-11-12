# Notas de la versión · EnvíaYa `calc`

## v2.1.0 · 11 de noviembre de 2026

**Novedad:** recargo de hora pico.

- Nuevo parámetro opcional `hora` (0 a 23). Se pasa por nombre: `calc(6, "urbana", "normal", 1, hora=18)`.
- Entre las 17:00 y las 19:59 (horas 17, 18 y 19) se cobra un recargo del 8 %, calculado después del recargo por zona.
- Si no se envía `hora`, el costo es el mismo de la v2.0.0: **es compatible hacia atrás**.
- Hora fuera de 0 a 23 → `ValueError("hora inválida")`.

## v2.0.0 · 11 de noviembre de 2026

**Versión con cambios incompatibles.** Lea esto antes de actualizar.

**Qué se rompe**
- `calc(..., flag=True)` ya no existe. Quien la llamaba con 6 argumentos recibe `TypeError`. Si necesita mostrar el costo, imprímalo desde el código que llama.
- Entradas que antes devolvían un costo ahora lanzan `ValueError`: peso mayor a 40 kg, zona distinta de urbana/rural/nacional y día fuera de 1 a 7.

**Qué se corrige (7 defectos)**
- Peso máximo 40 kg · recargo de sábado · solo el mayor descuento · redondeo correcto · validación de zona y día · mensaje con tilde.

**Impacto en los precios:** algunos costos cambian respecto a v1.0.0 porque ahora cumplen la especificación. Por ejemplo, 4 kg rural VIP en sábado con ENVIO10 pasa de $5.100 a $7.400.

**Calidad:** 61 pruebas automatizadas pasan, con 100 % de cobertura de sentencias y de ramas. La complejidad ciclomática de la función principal bajó de 14 a 1.