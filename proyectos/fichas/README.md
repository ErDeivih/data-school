# Fichas de proyecto · los cuatro CSV nuevos

**Qué es esta carpeta.** Cuatro **fichas de proyecto**, una por cada CSV que se añadió al catálogo
después de la importación inicial: telemetría de F1, cartera de acciones, clasificación de F1 y
partidos de fútbol. Cada ficha agrupa los proyectos del catálogo que usan ese CSV y fija qué
construir, con qué datos, cómo se verifica y qué se evalúa.

**Qué son y qué no son.** Son **enunciados verificables**, no implementaciones: en esta carpeta no hay
código de estos proyectos. Los dos proyectos completos siguen siendo
[PF-01](../pf-01-pulso-poblacion/README.md) y [PF-02](../pf-02-openf1/README.md). Una ficha describe
el trabajo y sus criterios de terminado; el código, los datos derivados y los resultados los produce
quien la resuelve.

**Base documental.** Los títulos, niveles y rutas de los proyectos salen de
[`proyectos/CATALOGO.md`](../CATALOGO.md); las filas, columnas y la descripción de cada CSV, de
[`datasets/CATALOGO.md`](../../datasets/CATALOGO.md) y
[`datasets/datasets.json`](../../datasets/datasets.json). La ficha de cada dataset, con procedencia y
checksum, está en [`datasets/FICHAS.md`](../../datasets/FICHAS.md). Este índice y las cuatro fichas se
escribieron el **2026-11-04**.

## Índice

| Ficha | CSV (filas × columnas) | Proyectos que cubre | Niveles | Tiempo total |
| --- | --- | --- | --- | --- |
| [telemetria-f1.md](telemetria-f1.md) | `telemetria-f1` (180 × 10) | P11, P12, P13 | intermedio | 19–25 h |
| [cartera-acciones.md](cartera-acciones.md) | `cartera-acciones` (360 × 3) | P14, P15, P16, P22 | básico a avanzado | 21–28 h |
| [f1-clasificacion.md](f1-clasificacion.md) | `f1-clasificacion` (400 × 12) | P17, P18, P19 | intermedio y avanzado | 19–25 h |
| [futbol-partidos.md](futbol-partidos.md) | `futbol-partidos` (380 × 12) | P20, P21 | intermedio y avanzado | 14–18 h |

Los cuatro CSV son sintéticos, de semilla fija y licencia CC0-1.0; su tamaño y checksum están en
[`datasets/CATALOGO.md`](../../datasets/CATALOGO.md).

## Cobertura del catálogo

Las cuatro fichas cubren **12 de los 22 proyectos** del catálogo: P11–P22. El resto queda en el
**backlog de fichas**:

- **P01–P10** (10 proyectos): sus datasets (`algoritmos-tiempos`, `clientes-churn`,
  `ventas-mensuales`, `encuestas-satisfaccion`, `precios-accion`, `sensores-planta`) no tienen ficha
  de proyecto propia en esta carpeta.
- Los **8 laboratorios (L01–L08)** tampoco tienen ficha aquí: son piezas cortas del portal, no
  proyectos con criterio de terminado.

**Nota de recuento.** El encargo hablaba de «18 fichas restantes», pero la cuenta no encaja con el
mapeo real: 22 proyectos − 12 cubiertos = **10 pendientes**. Salen 18 solo si se cuenta una ficha por
proyecto y se olvida que cada ficha agrupa varios; aquí una ficha = un CSV, no un proyecto.

## Cómo se leen las fichas

Todas comparten las mismas secciones, en el mismo orden: **Datos asignados**, **Proyectos del
catálogo que cubre**, **Nivel y rutas**, **Tiempo estimado**, **Enunciado**, **Datos y preparación**,
**Pasos**, **Criterios de terminado**, **Entregables**, **Qué demuestra y cómo se evalúa** y
**Riesgos típicos**.

- Los **criterios de terminado** son observables: describen una comprobación o un artefacto, no «que
  funcione».
- La **rúbrica** reparte 100 puntos entre datos, análisis, verificación y comunicación.
- El **tiempo estimado** es una horquilla de trabajo efectivo, no una promesa.

## Notas de encaje (leer antes de empezar)

Cuatro puntos donde el catálogo y el CSV asignado no encajan al pie de la letra. Las fichas los
declaran en lugar de inventar columnas:

1. **P17 pide una API y el dataset es un CSV.** En esta carpeta no hay API de F1. La ficha resuelve
   P17 como ingesta idempotente sobre un snapshot del CSV; la versión real con OpenF1 es
   [PF-02](../pf-02-openf1/README.md).
2. **P19 pide un undercut y `f1-clasificacion` no trae paradas, vueltas de carrera ni edad del
   neumático.** La ficha mide un proxy declarado (cambio de puestos entre clasificación y carrera) y
   remite a [telemetria-f1](telemetria-f1.md), que sí tiene la parada.
3. **P18, leído al pie de la letra, es una tautología:** `posicion_quali` es el rango de
   `vuelta_quali_s`, y esa vuelta es la suma de los sectores. La ficha convierte esa equivalencia en
   el control del proyecto y fija el objetivo aprendible en el puesto final de carrera.
4. **P22 habla de inflación y el CSV no la trae.** La ficha exige declarar la tasa asumida y separar
   lo que sale del fichero de lo que es supuesto; no se inventa un dato.

## Enlaces

- [Catálogo de proyectos y laboratorios](../CATALOGO.md)
- [Fichas de los 10 datasets](../../datasets/FICHAS.md)
- [Catálogo de datasets](../../datasets/CATALOGO.md)
- [README de proyectos](../README.md)
