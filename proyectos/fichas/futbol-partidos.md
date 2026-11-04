# Ficha · futbol-partidos — modelo en estrella y xG frente al marcador

**Estado:** ficha de enunciado. No hay implementación de este proyecto en la carpeta: aquí se fija
qué construir, con qué datos del catálogo y cómo se demuestra que está terminado. Las fichas
hermanas son [telemetria-f1](telemetria-f1.md), [cartera-acciones](cartera-acciones.md) y
[f1-clasificacion](f1-clasificacion.md).

## Datos asignados

- **CSV:** [`datasets/csv/futbol-partidos.csv`](../../datasets/csv/futbol-partidos.csv) — **380
  filas** y **12 columnas**; sintético, semilla fija y licencia CC0-1.0. Tamaño y checksum en
  [`datasets/CATALOGO.md`](../../datasets/CATALOGO.md).
- **Catálogo de proyectos:** [`proyectos/CATALOGO.md`](../CATALOGO.md) — cubre los proyectos P20 y
  P21.
- **Ficha del dataset:** [`datasets/FICHAS.md`](../../datasets/FICHAS.md) — procedencia, checksum y
  preguntas que permite responder.
- **Columnas:** `jornada`, `local`, `visitante`, `goles_local`, `goles_visitante`, `tiros_local`,
  `tiros_visitante`, `xg_local`, `xg_visitante`, `posesion_local`, `amarillas`, `resultado`.

## Proyectos del catálogo que cubre

| ID | Título del catálogo | Nivel |
| --- | --- | --- |
| P20 | Fútbol: ingesta y modelo en estrella | intermedio |
| P21 | Fútbol: el xG no es el marcador | avanzado |

## Nivel y rutas

- **P20:** intermedio, ruta **DE**. Ingesta, granularidad, dimensiones y conciliación de totales.
- **P21:** avanzado, ruta **DS**. Probabilidades de resultado, línea base, calibración e
  incertidumbre.
- **Requisitos previos:** SQL o pandas, modelo relacional básico (hecho y dimensiones), distribuciones
  de probabilidad y métricas de clasificación (log loss, Brier). P21 usa la tabla de P20.

## Tiempo estimado

| Proyecto | Horas |
| --- | --- |
| P20 | 6–8 h |
| P21 | 8–10 h |

Total de la ficha: **14–18 h**. P21 se apoya en el hecho por partido de P20; sin esa tabla, la mitad
del trabajo es limpieza repetida.

## Enunciado

El CSV describe 380 partidos de una liga sintética de veinte equipos con goles, tiros, xG, posesión y
tarjetas. Construye primero un modelo en estrella con un hecho por partido y dimensiones de equipo y
jornada, demostrando que los totales cuadran con el fichero original y que recargar no duplica nada
(P20). Después, usa ese hecho para responder qué parte del marcador es azar: estima probabilidades de
resultado con xG, compáralas con una línea base y con el marcador real, y explica qué se puede y qué
no se puede concluir (P21).

El detalle que hace difícil este dataset es que **las 380 filas no son 380 partidos independientes**:
son veinte emparejamientos repetidos diecinueve veces. Además, el `resultado` se deduce de los goles,
`posesion_local` implica la del visitante y `amarillas` es un total del partido, no de cada equipo. Un
modelo en estrella que ignore la granularidad, o una validación que ignore la repetición, produce
resultados que parecen buenos y no lo son.

## Datos y preparación

- **Estructura:** 380 filas = 38 jornadas × 10 partidos. Clave natural `(jornada, local, visitante)`,
  única y sin nulos. Veinte equipos aparecen 38 veces cada uno, pero **cada jornada tiene solo 16
  equipos distintos**: en cada jornada hay cuatro equipos que juegan dos veces. La parrilla no es una
  liga válida y no se puede construir una clasificación por jornadas con ella.
- **Repetición:** solo hay **20 emparejamientos distintos**, cada uno repetido **19 veces**, siempre en
  jornadas de la misma paridad (uno en las impares, otro en las pares). Son realizaciones distintas del
  mismo cruce, no partidos nuevos. Cualquier partición train/test debe agrupar por emparejamiento (o
  por jornada), nunca al azar por fila.
- **`resultado` es derivado:** coincide con los goles en las 380 filas (`1` gana local, `X` empate,
  `2` gana visitante). Se conserva como columna de conveniencia verificada, no como dato independiente.
- **`posesion_local`:** solo viene el porcentaje del local; el del visitante es `100 − posesion_local`.
  No hay columna separada que sumar.
- **`amarillas` es un total del partido**, no de cada equipo. En el modelo en estrella no se puede
  repartir entre local y visitante: se queda como atributo del hecho, y el README explica por qué.
- **xG y marcador no son lo mismo:** `xg_local` y `xg_visitante` son goles esperados (no enteros), y
  su suma no tiene por qué coincidir con el marcador. Esa diferencia es el objeto de P21, no un error
  a corregir.
- **Lo que no hay:** identidad de jugadores, tiros a puerta, xG por tiro, árbitro, estadio ni
  calendario real. La posesión, los tiros y las tarjetas son el único contexto disponible.

## Pasos

1. **Validar el crudo (P20).** Comprobar 380 filas, 12 columnas, clave única y ausencia de nulos;
   contar jornadas (38), equipos (20) y partidos por jornada (10).
2. **Auditar la parrilla (P20).** Demostrar con un informe que hay 20 emparejamientos repetidos 19
   veces y que cada jornada repite cuatro equipos; dejar constancia de que no se publicará una
   clasificación.
3. **Diseñar el esquema (P20).** Documentar granularidad y claves: `f_partido` (una fila por partido),
   `dim_equipo` (20 filas) y `dim_jornada` (38 filas); dos claves foráneas de equipo en el hecho.
4. **Cargar e idempotencia (P20).** Cargar el hecho y las dimensiones desde el CSV; recargar dos veces
   y demostrar que no hay duplicados y que los totales no cambian.
5. **Conciliar totales (P20).** Comprobar que la suma de goles, tiros y xG del hecho coincide con la
   del CSV, que no hay claves foráneas huérfanas y que cada partido tiene dos equipos distintos.
6. **Línea base de resultado (P21).** Calcular frecuencias de `1`/`X`/`2` y una línea base de goles
   esperados por equipo; evaluar con log loss y Brier en partición agrupada por emparejamiento.
7. **Modelo con xG (P21).** Convertir `xg_local` y `xg_visitante` en probabilidades de `1`/`X`/`2`
   (por ejemplo, Poisson con esas medias), comprobar que suman 1 y comparar con la línea base y con el
   marcador real.
8. **Suerte, calibración y verificación (P21).** Tabla por equipo de goles menos xG y de puntos
   reales frente a puntos esperados por xG, con intervalos agrupados por emparejamiento; calibración
   por bins. Cerrar con `verificar.py` (recuentos, conciliación e idempotencia), `README.md` con
   comandos y resultados, y una reejecución que produzca lo mismo.

## Criterios de terminado

- [ ] `verificar.py` comprueba 380 hechos, 20 equipos y 38 jornadas, 10 partidos por jornada y clave
      `(jornada, local, visitante)` única; devuelve código 0 solo si todo cuadra.
- [ ] El esquema está documentado con granularidad y claves: hecho por partido, dimensiones de equipo
      y jornada, dos referencias de equipo en el hecho y ninguna clave foránea huérfana.
- [ ] Recargar el CSV dos veces deja los mismos 380 hechos y la conciliación cuadra: suma de goles,
      tiros y xG del hecho = suma del CSV, `local != visitante` en los 380 partidos y la prueba está
      en `verificar.py`.
- [ ] `resultado` se recalcula desde los goles y coincide en 380/380 (el README lo declara derivado);
      `amarillas` se modela a nivel de partido, no repartida entre equipos, y se explica por qué.
- [ ] El informe de parrilla demuestra la repetición (20 cruces × 19) y la jornada con equipos
      repetidos, y el proyecto **no** publica una clasificación de liga.
- [ ] P21 compara línea base y modelo xG con log loss y Brier en partición agrupada por
      emparejamiento, y presenta calibración, no solo exactitud.
- [ ] La tabla de «suerte» por equipo va con incertidumbre y con la advertencia de que el xG del CSV
      no es una probabilidad de resultado ni un dato real.
- [ ] `README.md` reproduce todo con comandos; reejecutar produce los mismos resultados.

## Entregables

- Código: `cargar.py`, `esquema.sql` (o DDL equivalente), `verificar.py`, `modelo.py`.
- `data/f_partido.csv`, `data/dim_equipo.csv`, `data/dim_jornada.csv` y el crudo sin transformar.
- Informe de auditoría de la parrilla (repetición y equipos duplicados por jornada).
- Resultados de P21: tabla de probabilidades, comparación de métricas con intervalos, calibración y
  tabla de suerte por equipo.
- `README.md` con comandos, decisiones de modelado, supuestos y límites.
- Registro de comprobaciones de `verificar.py`.

## Qué demuestra y cómo se evalúa

Demuestra que sabes traducir una tabla plana a un modelo en estrella sin perder ni inventar filas,
que concilias totales contra el origen y que distingues un dato derivado de un hecho. En P21 demuestra
que no confundes xG con marcador, que usas una línea base y que comunicas la incertidumbre de una
liguilla de veinte cruces repetidos.

| Criterio | Peso |
| --- | --- |
| Ingesta, esquema y granularidad del modelo en estrella | 25 % |
| Idempotencia y conciliación de totales | 20 % |
| Auditoría de la parrilla y decisiones de modelado (`amarillas`, `resultado`) | 15 % |
| Línea base de P21 y comparación con el modelo xG | 20 % |
| Calibración, incertidumbre y lectura de «suerte» | 10 % |
| Documentación, límites y reproducibilidad | 10 % |

## Riesgos típicos

- **Pseudo-réplica:** tratar las 380 filas como partidos independientes y partir al azar. El mismo
  cruce cae en train y test y la métrica se infla.
- **Clasificación inventada:** sumar puntos por jornada cuando cada jornada tiene equipos repetidos y
  la parrilla no es una liga válida.
- **Fuga por `resultado`:** usarlo como feature al predecir el resultado. Es una función de los goles:
  o es el objetivo, o no entra.
- **xG = marcador:** presentar los goles esperados como goles, o corregir el marcador con xG como si
  el partido hubiera terminado de otra forma.
- **Atribuir `amarillas` a un equipo:** la columna es el total del partido; repartirla exigiría un
  dato que no existe.
- **Doble conteo de posesión:** sumar `posesion_local` y una supuesta posesión visitante que ya es
  `100 − posesion_local`.
- **Línea base ausente:** publicar log loss sin compararlo con la frecuencia de resultados ni con un
  modelo trivial; sin base, la métrica no dice si el modelo aporta.
