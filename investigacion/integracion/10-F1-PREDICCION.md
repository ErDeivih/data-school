# Predecir la clasificación y la carrera de F1: guía completa

**Fecha:** 2026-11-02 · **Nivel:** avanzado · **Proyecto:** P18 (clasificación) y P19 (undercut)

La pregunta es tentadora y el mercado está lleno de «predictores» que aciertan porque hacen trampa.
Esta guía explica cómo se construye uno honesto, qué se puede predecir de verdad y dónde se rompe.

---

## 1. Qué se puede predecir y qué no

| Objetivo | Dificultad | Por qué |
| --- | --- | --- |
| Orden de clasificación | Media | Depende casi todo del coche y de una vuelta limpia: hay señal |
| Ganador de la carrera | Alta | Una carrera son 60 vueltas con coche de seguridad, lluvia y abandonos |
| Podio | Media-alta | Más estable que el ganador, menos que la parrilla |
| Undercut | Media | Es una decisión estratégica con muchas variables ocultas |
| Abandono | Baja-media | Se puede estimar con fiabilidad histórica del equipo, no del piloto |

**Regla de oro:** si tu modelo acierta el ganador más del 60 % de las veces, sospecha. La parrilla
explica mucho; la carrera, poco.

## 2. Los datos (gratis)

| Fuente | Qué da | Límite |
| --- | --- | --- |
| [OpenF1](https://openf1.org/) | Sesiones, pilotos, vueltas, stints, boxes, posiciones, radio | Histórico desde 2023, límite de peticiones |
| [FastF1](https://docs.fastf1.dev/) | Telemetría, sectores, neumáticos, clima | Desde v3.9 pide F1TV Access |
| [Ergast](https://ergast.com/mrd/) (archivado) | Resultados históricos 1950-2024 | Sin mantenimiento; el espejo Jolpica lo sustituye |

Para empezar: OpenF1, tres temporadas, todas las carreras. Con 2023-2026 hay ~70 carreras y ~1.400
filas piloto-carrera, suficiente para un modelo simple.

## 3. El esquema de datos que necesitas

Un modelo en estrella, no un CSV con todo:

- `f_resultado_clasificacion`: grano piloto × carrera, con posición y tiempo de la mejor vuelta.
- `f_resultado_carrera`: grano piloto × carrera, con posición final, puntos y abandono.
- `f_vuelta`: grano piloto × carrera × vuelta, con duración, compuesto y edad del neumático.
- `dim_piloto`, `dim_equipo`, `dim_carrera`, `dim_circuito`.

Con eso, cualquier pregunta se responde con un `JOIN` y no con un `pivot` a mano.

## 4. Variables que sí y variables que no

**Sí (se conocen antes de la sesión):** circuito y su tipo, equipo, piloto, resultados previos en ese
circuito, rendimiento medio de las últimas 3 carreras, clima previsto, compuesto disponible.

**Sí (se conocen antes de la carrera, no antes de la clasificación):** posición de parrilla, tiempos
de clasificación, degradación estimada del stint.

**No, nunca:** posición final, puntos, abandono, tiempos de la carrera que quieres predecir. Es la
fuga clásica: el modelo aprende a leer la respuesta.

---

## 5. Clasificación: el modelo que sí funciona

1. **Línea base:** ordenar por la posición de la parrilla anterior y medir el error de orden. Sin
   esto no sabrás si el modelo aporta.
2. **Métrica:** para un orden, el error absoluto medio de puesto y la correlación de Spearman. Para
   el ganador, acierto top-1 y log-loss si das probabilidades.
3. **Modelo:** empieza por regresión ordinal o `HistGradientBoostingRegressor` con las variables de
   §4; no empieces por una red neuronal.
4. **Validación:** por carrera, nunca por fila. Entrena con las primeras 50 carreras y prueba con las
   últimas 10. Barajar filas mezcla pilotos de la misma carrera y regala información.
5. **Interpretación:** mira la importancia de variables. Si «equipo» domina, es correcto: en F1 el
   coche pesa más que el piloto.

## 6. Carrera: lo que de verdad mueve el resultado

Un modelo de ganador con las variables de parrilla acierta ~40 %. Para subir hay que modelar lo que
pasa durante la carrera:

- **Degradación por compuesto** (de `stints` y vueltas): pendiente en s/vuelta corregida por
  combustible. Sin corregir, la pendiente sale negativa porque el coche se aligera más de lo que se
  desgasta el neumático. Ese detalle es la mitad del proyecto.
- **Coste del pit stop** (tiempo medio perdido en boxes por circuito).
- **Probabilidad de coche de seguridad** por circuito y por clima.
- **Aguantar el undercut:** comparar el ritmo del que para antes con el que se queda, controlando
  compuesto y edad.

Con esas cuatro, un modelo de simulación (Monte Carlo sobre ritmo y paradas) explica más que
cualquier clasificador: no predice un ganador, da una distribución.

## 7. Errores que arruinan el proyecto

| Error | Consecuencia |
| --- | --- |
| Usar la posición final como variable | Acierto del 95 % y cero valor |
| Barajar filas para validar | Fuga entre pilotos de la misma carrera |
| Ignorar el efecto del combustible | La degradación sale negativa y la estrategia, al revés |
| Predecir el ganador y no dar incertidumbre | Un 40 % de acierto no es un pronóstico: es una moneda con sesgo |
| Mezclar temporadas con reglamentos distintos | El modelo aprende un reglamento que ya no existe |
| Optimizar con 20 carreras | Sobreajuste garantizado: 20 carreras no son una muestra |

## 8. Plan de cuatro semanas

| Semana | Qué | Entregable |
| --- | --- | --- |
| 1 | Ingesta OpenF1 y modelo en estrella | `f_vuelta` y `f_resultado` |
| 2 | Línea base y métrica de orden | Error de la parrilla sola |
| 3 | Modelo de clasificación con validación por carrera | Error por carrera y Spearman |
| 4 | Simulación de carrera con paradas y degradación | Distribución de posiciones, no un ganador |

Al final, el entregable no es «mi modelo acierta el 70 %»: es «mi modelo bate a la parrilla en X
puestos de media y estas son sus tres limitaciones».

---

## 9. Dónde está esto en la escuela

Proyecto P18 (clasificación) y P19 (undercut) en `sitio/proyectos.js`. Lecciones:
`fuga-de-datos`, `validacion-temporal`, `purged-kfold`, `metricas-de-regresion`,
`ingenieria-de-features`, `simulacion-de-monte-carlo`, `calibracion` y `causalidad-vs-correlacion`.

Y el código de partida real: `proyectos/pf-02-openf1/`, con 3.029 vueltas y la degradación por
compuesto ya calculada.
