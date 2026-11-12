# Changelog

Todos los cambios importantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.0.0] - 2026-11-11

### Changed
- **BREAKING:** se eliminó el argumento `flag` de `calc`; la función ya no imprime el costo.
- **BREAKING:** las entradas inválidas (peso mayor a 40 kg, zona desconocida, día fuera de 1 a 7) ahora lanzan `ValueError` en lugar de devolver un costo.
- La función principal se llama `calcular_costo`; `calc` se conserva como alias.
- Refactorización: funciones extraídas, constantes con nombre en lugar de números mágicos y patrón Estrategia para el recargo por zona (`EstrategiaZona`, `ZonaUrbana`, `ZonaRural`, `ZonaNacional`).

### Fixed
- DEF-01: el peso máximo era 50 kg; ahora es 40 kg (PMAX).
- DEF-02: el sábado no cobraba el recargo de fin de semana.
- DEF-03: se acumulaban el descuento del cliente y el del cupón; ahora se aplica solo el mayor.
- DEF-04: el redondeo truncaba; ahora redondea al múltiplo de $100 más cercano y los $50 suben.
- DEF-05: una zona inválida no lanzaba error.
- DEF-06: un día fuera de 1 a 7 no lanzaba error.
- DEF-07: el mensaje de error decía "peso invalido" sin tilde.

### Removed
- Argumento `flag` y el diccionario global `CONFIG`.

## [1.0.0] - 2026-11-11

### Added
- Código heredado de EnvíaYa (`calc`) con la configuración del estudiante 0182220060.

[Unreleased]: https://github.com/TU_USUARIO/envios-ya/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Vicenz111/envios-ya/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Vicenz111/envios-ya/releases/tag/v1.0.0